import json
from util import sha256, sign, verify
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
        return verify(self.signature, body, self.public_key)

    def double_spends(self, public_key, inflows):
        for i in BLOCKS:
            if not(i.double_spends(public_key, inflows.get_blockId(), inflows.get_txnId())):
                return False
        return True


    def verify(self, block_chain):
        if not self.txn_signature_verified():
            print("****SIGNATURE FAILED TO VERIFY****")
            return False
        total_money = 0

        # TODO Make sure every value in inflows is unique

        #Get Total amout Requested
        for inflow in self.inflows:
            for block in block_chain:
                for txn in block.transactions:
                    #Check for double spending
                    for inflow_other in txn.inflows:
                        if (inflow_other.owner == inflow.owner
                            and inflow_other.block_id == inflow.block_id
                            and inflow_other.txn_idx == inflow.txn_idx):
                            print("*** DOUBLE SPENDING***")
                            return False
                    #Get Total Spent
                    for outflow in txn.outflows:
                        if outflow.recipient == inflow.owner:
                            total_money += outflow.coins

        total_out = 0
        for outflow in self.outflows:
            total_out += outflow.coins

        if total_money != total_out:
            print("****MONEY AMOUNT DOES NOT MATCH****")
            return False
        return True

if __name__ == '__main__':
    main()
