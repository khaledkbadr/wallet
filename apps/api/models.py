from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator


class AccountBalance(models.Model):
    """Account Balances

    mainly used to lock accounts and cache balances
    """

    account = models.CharField(max_length=50, primary_key=True)
    balance = models.DecimalField(
        max_digits=20, decimal_places=2, validators=[MinValueValidator(Decimal("0.0"))]
    )
    currency = models.CharField(max_length=3, default="USD")

    def __str__(self):
        return "{}'s balance: {} USD".format(self.account, self.balance)


class Transfer(models.Model):
    """
    For every money transfer between two account.
    Two Transfer objects are created every time with different direction and primary and secondary accounts
    """

    DIRECTIONS = [("incoming", "incoming"), ("outgoing", "outgoing")]

    primary_account = models.ForeignKey(
        AccountBalance, on_delete=models.CASCADE, related_name="transfers"
    )
    secondary_account = models.ForeignKey(AccountBalance, on_delete=models.CASCADE)
    direction = models.CharField(max_length=8, choices=DIRECTIONS)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    timestamp = models.DateTimeField()

    def __str__(self):
        if self.direction == "outgoing":
            return "{} transfered {} USD to {}".format(
                self.primary_account, self.amount, self.secondary_account
            )
        else:
            return "{} got {} USD from {}".format(
                self.primary_account, self.amount, self.secondary_account
            )
