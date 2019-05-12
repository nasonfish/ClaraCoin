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



def getMoney(public_key):
    #Return the amount of clara coin attached to public key
    return (transactions)
def howMuchMoneyDoIHave(public_key):
    #return amount of money user has
    return

def verifyMoney(public_key, amount_spend):
    # Return true if transaction money is less than getMoney
    return getMoney(public_key) > amount_spend


if __name__ == '__main__':
    userInterface()
