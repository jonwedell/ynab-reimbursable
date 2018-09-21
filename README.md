### Usage

Run reimbursable.py and follow the prompts. Get your bearer token from the
[developer settings page](https://app.youneedabudget.com/settings/developer) (you must be signed in to your YNAB account).
Click "New Token" and then copy the displayed bearer token.

For this tool to work properly, you must follow the following rules when creating reimbursable transactions:

* Have a dedicated category that you use to track reimbursable expenses.
Make sure to set the appropriate category or subcategory when entering transactions.
* Always set the payee for a reimbursable transaction or subtransaction.
* Once a transaction has been repaid, flag it "green". The tool ignores green transactions.
* Set a goal for your reimbursable category equal to the original funding level.
This allows the tool to determine if your outstanding balance is not properly accounted for in YNAB.

### Coming next

A future version will provide a mechanism to automatically mark all transactions from a given payee as repaid.

### FAQ

Q: How do I change which budget or category the tool looks at?
A: Delete config.ini and re-run the tool.

Q: What if I paid Bob on behalf of Bill and I want the reimbursable transaction to show Bob as the payee rather than Bill?
A: Make a split transaction with the main payee set to Bob, but the split record payee set to Bill. (You can have a split transaction with only one split.)

