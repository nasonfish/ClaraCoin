import json
from util import sha256, sign, verifySignature
from chain import InFlow, OutFlow

class Transaction():
    def __init__(self, public_key, inflows, outflows, signature):
        self.public_key = public_key
        self.inflows = inflows
        self.outflows = outflows
        self.signature = signature


    def serialize(self):
        return { "hash": self.get_hash(),
                 "data": { "signature": self.signature,
                           "body": { "public_key": self.public_key,
                                     "inflows": [ inflow.serialize() for inflow in self.inflows ],
                                     "outflows": [ outflow.serialize() for outflow in self.outflows ]
                                   }
                         }
                }

    @staticmethod
    def build_signed_txn(public_key, inflows, outflows, signing_key):
        body = { "public_key": public_key, "inflows": [ inflow.serialize() for inflow in inflows ], "outflows": [ outflow.serialize() for outflow in outflows ] }
        signature = sign( json.dumps(body), signing_key )
        return Transaction( public_key, inflows, outflows, signature )

    @staticmethod
    def load(obj):
        if type(obj) == str:
            obj = json.loads(obj)

        return Transaction( obj["data"]["body"]["public_key"],
                            [ InFlow.load(l) for l in obj["data"]["body"]["inflows"] ],
                            [ OutFlow.load(l) for l in obj["data"]["body"]["outflows"] ],
                            obj["data"]["signature"]
        )

    def get_hash(self):
        data = { "signature": self.signature,
                 "body": {
                     "public_key": self.public_key,
                     "inflows": [ inflow.serialize() for inflow in self.inflows ],
                     "outflows": [ outflow.serialize() for outflow in self.outflows ]
                 }
        }
        return sha256( json.dumps( data ).encode("ascii") )

    # TODO this method is to be used for pruning transactions
    def is_spent(self, blockchain):
        for outflow in self.outflow:
            if not outflow.is_spent():
                return False
        return True

    def txn_signature_verified(self):
        body = { "public_key": self.public_key, "inflows": [ inflow.serialize() for inflow in self.inflows ], "outflows": [ outflow.serialize() for outflow in self.outflows ] }
        return verifySignature( self.signature, body, self.public_key )

    # TODO clean this up
    '''Validates the transaction, which means checking for three things:
            i) transaction signature verifies
            ii) no double spending occurs; every inflow refers to an unspent outflow in the chain
            iii) total incoming amount equals total outgoing amount'''
    def verify(self, blockchain, outer_block=None):
        print("Validating transaction...")
        if not self.txn_signature_verified():
            print("Transaction signature failed to verify")
            return False

        # TODO Make sure every value in inflows is unique
        '''
        # Get Total amout Requested
        for inflow in self.inflows:
            for block in blockchain.blocks:
                for txn in block.transactions:
                    # Check for double spending
                    for inflow_other in txn.inflows:
                        if (inflow_other.owner == inflow.owner
                                and inflow_other.block_id == inflow.block_id
                                and inflow_other.txn_idx == inflow.txn_idx):
                            print("*** DOUBLE SPENDING***")
                            return False
                    # Get Total Spent
                    for outflow in txn.outflows:
                        if outflow.recipient == inflow.owner:
                            total_money += outflow.coins

        total_out = 0
        for outflow in self.outflows:
            total_out += outflow.coins
        '''

        total_out = sum(outflow.coins for outflow in self.outflows)

        inflows = []
        for block in blockchain.blocks:
            if outer_block and block.block_idx == outer_block.block_idx:
                break
            for i in range(len(block.transactions)):
                txn = block.transactions[i]
                for outflow in txn.outflows:
                    if outflow.recipient == self.public_key:
                        inflows.append((InFlow(self.public_key, block.block_idx, i), outflow.coins))
        for block in blockchain.blocks:
            if outer_block and block.block_idx == outer_block.block_idx:
                break
            for i in range(len(block.transactions)):
                txn = block.transactions[i]
                for inflow in txn.inflows:
                    for accounted in inflows:  # bad searching. oh well. blockchain is slow anyway
                        if accounted[0].txn_idx == inflow.txn_idx and accounted[0].block_id == inflow.block_id:
                            inflows.remove(accounted)
        inflows, total_money = [f[0] for f in inflows], sum(b[1] for b in inflows)

        if total_money != total_out:
            print("****MONEY AMOUNT DOES NOT MATCH (total: {}, out: {})****".format(total_money, total_out))
            return False
        return True
