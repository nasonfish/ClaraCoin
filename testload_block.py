from chain import Block
import json
import pprint

import txn


with open("Blocks_updated/block0.json", 'rb') as f:
    f_bytes = f.read()
    # obj_dict = json.loads(f_bytes.decode( "ascii" ))
    # print(obj_dict["transactions"])
    block = Block.load( f_bytes.decode( "ascii" ))
    #print( json.dumps(block.serialize()) )
    # block = Block(obj_dict["prev_block"], [ Transaction.load( txn ) for txn in obj_dict["transactions"] ], obj_dict["block_idx"], obj_dict["magic_num"], obj_dict["merkleroot"])
    # print(block)
