from chain import Block, BlockChain, InFlow, OutFlow, Transaction
from initial_user import getInitialUser
#Get block chain


PUBLIC_USER_ROOT = "75efa6f1fdf1393a5ea815b2b3690293d079df187944f22ec79f3380ef7bd743"
PRIVATE_USER_ROOT = "1d82897e5881368cac9eb99126cdfca1e0317629dbeaa7280484c5dae81e932b"

PUBLIC_USER_OTHER = "ee00e543db3b7b5508821b211151d7cea8187613f25bcf3037bbb38bfa7c4dc7"
PRIVATE_USER_OTHER = "7ed318d6602e38caa1a519efb26662a2ad7aa133fbf13d4ed9d09dfc5b58f9b6"


block0 = getInitialUser()
print(type(block0))
blockchain = BlockChain([block0])
## TEMP fix to get block object

def userInterface():
    #Check for valid public key
    while True:
        private_key = input("Enter your private key")
        try:
            if(len(private_key) != 64):
                raise (ValueError("Incorrect Length of Private key"))
            int(private_key, 16)
        except:
            print("Please enter a valid private key")
            continue

        user_public_key = input("Enter your private key")
        try:
            if(len(user_public_key) != 64):
                raise (ValueError("Incorrect Length of Private key"))
            int(user_public_key, 16)
        except:
            print("Please enter a valid private key")
            continue

        recip_public_key = input("Enter public key of Recipient")
        try:
            if(len(recip_private_key) != 64):
                raise (ValueError("Incorrect Length of Public key"))
            int(recip_private_key, 16)
        except:
            print("Please enter a valid public key")
            continue
        amount_spend = input("Enter amount of Clara Coin to be transfered")
        try:
            if (amount_spend != str(int(amount_spend)) and amount_spend < 1):
                raise (ValueError("Entered value isn't positive whole number"))
            break
        except:
            print("Please enter a positive, whole number amount")
            continue
    #Create transaction
    inflows, outflows = balance(blockchain, user_public_key, recip_public_key, amount_spend)
    txn = Transaction.build_signed_txn(user_public_key, inflows, outflows, private_key)
    print(txn.serialize())


def balance(blockchain, public_key):
    """Get all the money associated with a public key within a particular blockchain"""
    total = 0
    inflows = []
    for block in blockchain.blocks:
        for i in range(len(block.transactions)):
            txn = block.transactions[i]
            for outflow in txn.outflows:
                if outflow.recipient == public_key:
                    inflows.append(InFlow(public_key, block.block_idx, i))
                    total += outflow.coins
            for inflow in txn.inflows:
                for accounted in inflows:  # bad searching. oh well. blockchain is slow anyway
                    if accounted.txn_id == inflow.txn_id:
                        inflows.remove(accounted)
                        total -= accounted.coins
    return inflows, total

# TODO all of these have the blockchain argument. maybe they belong
# in the blockchain class
def build_flows(blockchain, from_public, to_public, amount):
    inflows, total = balance(blockchain, from_public)
    outflows = []
    if total < amount:
        raise Exception("You can't send more money than you own.")
    if total > amount:
        outflows.append(OutFlow(total-amount, from_public)) # send to self
    outflows.append(OutFlow(amount, to_public)) # send to target
    return inflows, outflows

if __name__ == '__main__':
    inflows, total = balance(blockchain, PUBLIC_USER_ROOT)
    inflows, outflows = build_flows(blockchain, PUBLIC_USER_ROOT, PUBLIC_USER_OTHER, 5000)
    txn = Transaction.build_signed_txn(PUBLIC_USER_ROOT, inflows, outflows, PRIVATE_USER_ROOT)
    print(txn.serialize())
