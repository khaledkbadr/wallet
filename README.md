# Wallet Service

Wallet Service provides RESTful API to add and list account balances as well as making transfers between the accounts and view them

## How to run

To  run Wallet Service you have to set `SITE_HOST`, `POSTGRES_HOST`, `POSTGRES_PASSWORD`, `POSTGRES_USER`, `POSTGRES_DB` env variable and run `docker-compose up` or simple modify [dev.sh](./bin/dev.sh) with current and run `./bin/dev.sh up`

> `SITE_HOST` is the allowed host value that you must access the service with. To run locally, please set `127.0.0.1 <SITE_HOST>`
to your `/etc/hosts` file to access the service

## API documentation

There are three ways to check API documentation

* Find the OpenAPI spec in [schema.yml](./docs/schema.yml)
* Check [examples.http](./docs/examples.http) for request examples

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
