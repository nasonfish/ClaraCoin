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
                                                  "inflows": [inflow.serialize() for inflow in self.inflows],
                                                  "outflows": [outflow.serialize() for outflow in self.outflows] }
                                       }
                            }


    @staticmethod
    def build_signed_txn(public_key, inflows, outflows, signing_key):
        body = { "public_key": public_key, "inflows": [inflow.serialize() for inflow in inflows], "outflows": [outflow.serialize() for outflow in outflows] }
        signature = sign(json.dumps(body), signing_key)
        return Transaction(public_key, inflows, outflows, signature)

    @staticmethod
    def load(inp):
        if type(inp) == str:
            inp = json.loads(inp)
        # self.public_key = obj_dict["data"]["body"]["public_key"]
        # self.inflows = obj_dict["data"]["body"]["inflows"]
        # self.outflows = obj_dict["data"]["body"]["outflows"]

        # self.inflows = []
        # for i in self.txn[1][1]:
        #    self.inflows.append(InFlow(self.get_public_key(), *i))
        # self.outflows = []
        # for i in self.txn[1][2]:
        #    self.outflows.append(OutFlow(*i))
        return Transaction(
            inp["data"]["body"]["public_key"], 
            [InFlow.load(l) for l in inp["data"]["body"]["inflows"]], 
            [OutFlow.load(l) for l in inp["data"]["body"]["outflows"]], 
            inp["data"]["signature"]
        )

    def get_hash(self):
        data = {
            "signature": self.signature,
            "body": { 
                "public_key": self.public_key, 
                "inflows": [inflow.serialize() for inflow in self.inflows], 
                "outflows": [outflow.serialize() for outflow in self.outflows] 
            }
        }
        return sha256( json.dumps( data ).encode("ascii") )

    def is_spent(self, blockchain):
        # for each outflow in this transaction, go through all blocks that were
        # mined later than that which this transaction is included in, and
        # see if there is an inflow pointing back to the outflow
        for outflow in self.outflow:
            if not outflow.is_spent():
                return False
        return True

    def txn_signature_verified(self):
        body = { "public_key": self.public_key, "inflows": [inflow.serialize() for inflow in self.inflows], "outflows": [outflow.serialize() for outflow in self.outflows] }
        return verifySignature(self.signature, body, self.public_key)


    def verify(self, blockchain, outer_block=None):
        print("verifying block")
        if not self.txn_signature_verified():
            print("****SIGNATURE FAILED TO VERIFY****")
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
