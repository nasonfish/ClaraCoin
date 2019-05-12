from chain import BlockChain, Block, Transaction, Confirmation, BlockChainRequest

data_types = {b'1': BlockChain, b'\x02': Block, b'\x03': Transaction, b'\x04': Confirmation, b'\x05': BlockChainRequest}

def send_format(data):
    """Transform an object in data_types into its corresponding JSON serialization 
    (with metadata to be understood by recv_format())"""
    for i in data_types:
        if type(data) == data_types[i]:
            return i + data.serialize().encode('ascii')
    return None

def shout(sock, data):
    raw = None
    if type(data) is bytes:
        raw = data
    elif type(data) is str:
        raw = data.encode('ascii')
    else:
        raw = send_format(data)
    if not raw:
        raise Exception("I don't know how to send data over the wire: " + data)
    sock.send(raw + b'\n')

def recv(data):
    """Given data we have received over the wire, transform it back into
    an object."""
    ident = data[0].encode('ascii')
    if ident in data_types:
        dt = data_types[ident]
        return dt.load(data[1:])
    # unknown
    return None

