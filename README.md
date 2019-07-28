# Wallet Service

## Enhancements

* I have linked double-entry bookkeeping rows with the timestamp but it's hard to track with naked eye. so I believe it would've been better to use a Journal model and the two transfer rows in Tranfer model should be related to a row in Journal.  so it can be easier to track with

For example Journal Entry would be like below

```info
    id: 1
```

and the transfer rows would be

```info
    primary_account: "bob",
    direction: "outgoing",
    amount: 10,
    secondary_account: "jack",
    journal_id: 1,

    primary_account: "jack",
    direction: "ingoing",
    amount: "10",
    secondary_account: "bob",
    journal_id: 1,
```

This is the simplest for I can do this. It can also be done with a pregenerated ids bucket for each transfer in order to avoid concurrency problems.
