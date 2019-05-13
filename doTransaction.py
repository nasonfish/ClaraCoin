from chain import transaction, Block, BlockChain
from initial_user import getInitialUser
#Get block chain


PUBLIC_USER_ROOT = "75efa6f1fdf1393a5ea815b2b3690293d079df187944f22ec79f3380ef7bd743"
PRIVATE_USER_ROOT = "1d82897e5881368cac9eb99126cdfca1e0317629dbeaa7280484c5dae81e932b"

PUBLIC_USER_OTHER = "ee00e543db3b7b5508821b211151d7cea8187613f25bcf3037bbb38bfa7c4dc7"
PRIVATE_USER_OTHER = "7ed318d6602e38caa1a519efb26662a2ad7aa133fbf13d4ed9d09dfc5b58f9b6"


block0 = getInitialUser()
print(type(block0))
BlockChain = BlockChain([block0])
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
    return (private_key, user_public_key, recip_public_key, amount_spend)



def balance(public_key):
    """Get all the money associated with a public key within a particular blockchain"""
    total = 0
    transactions = []
    print(BlockChain.blocks)
    for block in BlockChain.blocks:
        for txn in block.transactions:
            print(type(txn))
            for outflow in txn.outflows:
                print(outflow)
                if outflow.recipient == public_key:
                    transactions.append(outflow)
                    total += outflow.coins
            for inflow in block.inflows:
                for accounted in transactions:  # bad searching. oh well. blockchain is slow anyway
                    if accounted.id == inflow.txn_id:
                        transactions.remove(accounted)
                        total -= accounted.coins
    return transactions, total

def howMuchMoneyDoIHave(public_key):
    print("You have", str(balance(public_key)[1]))
    return

def verifyMoney(public_key, amount_spend):
    #Calculate difference between totalMoney and money being spent
    totalMoney = balance(BlockChain, public_key)[1]
    validTxn = total_money > amount_spend
    moneyToSelf = totalMoney - amount_spend
    return(validTxn, moneyToSelf)

def calcOutflow(user_public_key, recip_public_key, moneyToSelf, amount_spend):
    outflow = []
    if moneyToSelf != 0:
        outflow.append('"outflows": [{"recipient": user_public_key,"number_of_coins": moneyToSelf}]')
    outflow.append('"outflows": [{"recipient": recip_public_key,"number_of_coins": amount_spend}]')
    return


# TODO all of these have the blockchain argument. maybe they belong
# in the blockchain class
def build_flows(blockchain, from_public, to_public, amount):
    transactions, total = balance(BlockChain, from_public)
    for i in transactions:
        InFlow()


if __name__ == '__main__':
    howMuchMoneyDoIHave(PUBLIC_USER_ROOT)
