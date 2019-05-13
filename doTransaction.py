from chain import transaction

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



def balance(blockchain, public_key):
    """Get all the money associated with a public key within a particular blockchain"""
    total = 0
    transactions = []
    for block in blockchain.blocks:
        for outflow in block.outflows:
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
    print("You have", str(balance(blockChain, public_key)[1]))
    return

def verifyMoney(public_key, amount_spend):
    #Calculate difference between totalMoney and money being spent
    totalMoney = balance(blockChain, public_key)[1]
    validTxn = total_money > amount_spend
    moneyToSelf = totalMoney - amount_spend
    return(validTxn, moneyToSelf)

def calcOutflow(user_public_key, recip_public_key, moneyToSelf, amount_spend):
    outflow = []
    if moneyToSelf != 0:
        outflow.append(
        #Something like this
            "outflows": [
    		{
    			"recipient": user_public_key,
    			"number_of_coins": moneyToSelf
    		}
    outflow.append(
    "outflows": [
    {
        "recipient": recip_public_key,
        "number_of_coins": amount_spend
    }

# TODO all of these have the blockchain argument. maybe they belong
# in the blockchain class
def build_flows(blockchain, from_public, to_public, amount):
    transactions, total = balance(blockchain, from_public)
    for i in transactions:
        InFlow()


if __name__ == '__main__':
    #Verify Money
    print("some functions should be here")
