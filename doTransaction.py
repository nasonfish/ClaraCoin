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



def balance(blockChain, public_key):
    # Return the amount of clara coin attached to public key
    totalMoney = 0
    transactions = []
    for block in blockChain.blocks:
        for outflow in block.outflows:
            if (outflow.recipient == public_key):
                transactions.append(outflow)
                totalMoney += `money

    return (transactions, totalMoney)

def howMuchMoneyDoIHave(public_key):
    print("You have", str(balance(blockChain, public_key)[1]))
    return

def verifyMoney(public_key, amount_spend):
    #Calculate difference between totalMoney and money being spent
    totalMoney = balance(blockChain, public_key)[1]
    validTxn = total_money > amount_spend
    moneyToSelf = totalMoney - amount_spend
    return(validTxn, moneyToSelf)

def calcOutflow(moneyToSelf, amount_spend):
    outflow = []
    if moneyToSelf != 0:
        outflow.append( #An outflow of the remaining money to one self)
    outflow.append(#An outflow of amount spend to oneself)
if __name__ == '__main__':
    #Verify Money
