Challenge Bugdget
=================

This challenge presents a user with a budget planning application.
The application asks the user to enter their total income and expenses
over a handful of months. We then compute the net savings (income minus
expenses) for each month entered.

The application then switches into "forecast" mode -- we identify the
trend in monthly savings by fitting a linear regression, then
forecast the bank account's balance into the future.

The key is to manufacture a negative-sloped savings line, which will
underflow the bank account balance to +MAX_INT. The underflow occurs
on the following lines:

```python
expected_savings = np.uint32(last_known_bank_account_balance) + np.uint32(slope) * count_months_to_predict
```

Note that your bank account balance must be positive before entering
forecasting mode, or else the program quits.
