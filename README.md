## Instructions

Ensure you have both docker and docker-compose installed. Go to the project root and run the following command.

```
$ docker-compose up
```

### Troubleshooting

I've noticed some odd errors with docker-compose on windows based machines - if you're seeing database related errors in the logs, odds are the `depends` key in the configs aren't being respected. Cleaning the slate and restarting seems to work well.

```
$ docker-compose down --volume && docker-compose build --no-cache && docker-compose stop && docker-compose rm -f && docker-compose up
```

### To provide alternative input via json

The project provides a script which will convert a list of newline seperated users and their addresses in the following
format to json:

```
satoshi nakamoto: address
Mark Karpelès: address
```

To use: execute the script, pipe the output to some file, and update the config

```
# Open your editor of choice and drop the users to index for in some file
$ vim users.txt

# Add permissions
$ chmod +x users_to_json.py

# Drop the results in json_input as only it's contents are copied to the image
$ ./users_to_json.py users.txt > json_input/users.json

# Update the env variabe JSON_USERS_FILE to the new path
$ vim infrastructure/docker-compose/env.dev
```


## Structure

The challenge was completed using python with the django framework. Django was chosen primarly due to familiarity with
it's ORM for quick scaffolding.

The django project contains 2 modules, the default `kraken_takehome` and `transaction_processor` apps. The project's
implementation per the challenge lives in `transaction_processor` while `kraken_takehome` implements settings and
contains some boilerplate for admin functions ( rendered useless due no ports being exposed and no server instance set
to spin. The docker-compose config is set to run a django command which will index the input provided and spit the
results in the preset format.

## Improvements

* **Add a scheduler**: This project is designed to consume one off inputs via files in the container. We could easily
  modify the transaction processor module to consume live input the bitcoin daemon with the help of a scheduler (
  typically something like celery is used for this purpose ) which would routinely call some endpoint such as
  `listsinceblock`.
* **Listen to ZMQ Notifications**: Bitcoind's rpc server is notoriously easy to overwhelm, especially during times of
  network stress. We could avoid this possible vector of error by instead listening to notifications provided by the ZMQ
  sockets. Downsides: Extra work will have to performed to decode block/transactional data, and the listener must be
  resilient to duplicates.
* **Explicit tables for transaction outputs**: At the moment this implementation has a list of outputs in the mildly
  misnamed "Transactions" table, with a unique_together constraint on the txid and vout index. This performs well for
  the current usecase, which largely ignores the output index and focuses on uniqueness between the outputs on a
  transaction. However this is not always ideal. The current implementation does not make queries against this output
  index easy/efficient, and adds additional complexities when performing necessary actions such as sweeping, sending.
  Explicitly moving these outputs to their own 1st class table will allow for more flexibility in future usecases.

