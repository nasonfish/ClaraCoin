from chain import transaction

def transfercoin():
    #Check for valid public key
    while True:
        private_key = input("Enter private key")
        try:
            int(private_key, 16)
        except:
            print("Please enter a valid private key")
            pass

        public_key = input("Enter public key of Recipient")
        try:
            int(private_key, 16)
        except:
            print("Please enter a valid private key")
            pass

        amount = input("Enter amount of Clara Coin to be transfered")
        try:
            int(private_key, 16)
        except:
            print("Please enter a valid private key")
            pass
        catch:
            int(public_key, 16)


    "1d82897e5881368cac9eb99126cdfca1e0317629dbeaa7280484c5dae81e932b"
