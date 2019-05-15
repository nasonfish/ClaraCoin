# ClaraCoin

A Cryptocurrency that is pretty okay sometimes

## Installation

Python 3.6 is recommended for running this software (since dictionaries are consistently ordered, there isn't a risk of signatures not verifying for strange reasons).

## Use

You need a bunch of terminal windows open to test this out.

1. Run `./run_server.sh`
    - Run the dumb server which simply `wall`s messages that are received
2. Run `./run_miner.sh`
    - Run a miner, which connects to the server (port 1264) and sends a request for the blockchain status from another miner
3. Run `./initialize_miner.sh`
    - This simulates another miner sharing a blockchain with the miner who just connected.
4. Run `./simulate_transaction.sh`
    - This creates a new transaction and sends it to the server, so the miner will pick up the block and try to mine it.


## Caveats

 - Miners get no reward for mining
 - Multiple miners is sketchy-- overlapping messages can confuse them and make everyone crash
 - Sharing a mined block with other miners may hang on validation for an unknown reason
 - Forking is easy to force, and there is not a good mechanism in place to count confirmations or protect from this.

That being said, this is a great proof-of-concept of building a blockchain through a decentralized-ish network, where transactions are announced and blocks are mined successfully.
