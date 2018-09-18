#!/usr/bin/python3

import os
try:
    import requests
except ImportError:
    print('Please run "pip3 install requests" before running.')
import configparser

ynab_root = 'https://api.youneedabudget.com/v1/budgets'
dir_path = os.path.dirname(os.path.realpath(__file__))
ini_path = os.path.join(dir_path, 'config.ini')

# Load/set up the configuration
config_change = False
config = configparser.ConfigParser()
config.read(ini_path)

if 'default' not in config:
    config['default'] = {}
    config_change = True

if 'bearer' not in config['default']:
    config['default']['bearer'] = input('Please enter the bearer token: ')
    config_change = True
ynab_headers = {"Authorization": "Bearer %s" % config['default']['bearer']}

if 'budget' not in config['default'] or not config['default']['budget']:
    budgets = requests.get(ynab_root, headers=ynab_headers).json()['data']['budgets']
    for pos, budget in enumerate(budgets):
        print("%s) %s" % (pos + 1, budget['name']))
    config['default']['budget'] = budgets[int(input('Please enter the number for the budget you want to use: '))-1]['id']
    config_change = True
ynab_root += '/' + config['default']['budget'] + '/'

if 'category' not in config['default'] or not config['default']['category']:
    category_id_map = {}
    enumerator = 1
    category_groups = requests.get(ynab_root + 'categories', headers=ynab_headers).json()['data']['category_groups']
    for category_group in category_groups:
        if category_group['name'] == 'Credit Card Payments' or category_group['name'] == 'Internal Master Category':
            continue
        for category in category_group['categories']:
            if not category['hidden'] and not category['deleted']:
                category_id_map[enumerator] = category['id']
                print("%s) %s" % (enumerator, category['name']))
                enumerator += 1
    category_id = int(input('Please enter the number for the category you use as reimbursable: '))
    config['default']['category'] = category_id_map[category_id]
    config_change = True

if config_change:
    with open(ini_path, 'w') as config_file:
        config.write(config_file)


# Now get the actual unpaid transactions
transactions = requests.get(ynab_root + 'categories/%s/transactions' % config['default']['category'],
                            headers=ynab_headers).json()['data']['transactions']

transaction_dictionary = {}
for transaction in transactions:
    if transaction['flag_color'] != 'green' and not transaction['deleted']:
        if transaction['payee_name'] not in transaction_dictionary:
            transaction_dictionary[transaction['payee_name']] = [transaction]
        else:
            transaction_dictionary[transaction['payee_name']].append(transaction)

total_outstanding = 0
for payee in transaction_dictionary.keys():
    transactions = transaction_dictionary[payee]
    owed = sum(x['amount'] for x in transactions)
    total_outstanding += owed
    print("%s: $%.2f" % (payee, owed / -1000))
    for transaction in transactions:
        print("\t%s: $%.2f" % (transaction['memo'], transaction['amount'] / -1000))

category_data = requests.get(ynab_root + 'categories/%s' % config['default']['category'],
                             headers=ynab_headers).json()['data']['category']
print('Total outstanding: $%.2f' % (total_outstanding / -1000))
print('Remaining Funds: $%.2f' % (category_data['balance'] / 1000))

if category_data['goal_target']:
    reconciliation = category_data['balance'] - (category_data['goal_target'] + total_outstanding)
    if reconciliation < 0:
        print('Missing funds: $%.2f' % (reconciliation / -1000))
    else:
        print('Overfunded: $%.2f' % (reconciliation / 1000))
else:
    print('Would check funds match if reimbursable goal funding set.')