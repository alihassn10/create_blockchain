# Importing libraries

import datetime
import hashlib
import json
from flask import Flask, jsonify

# Building blockchain
class Blockchain:
    def __init__(self):
        self.chain=[]
        # creating genesis block
        self.create_block(proof=1,prev_hash='0')
        
    def create_block(self, proof, prev_hash):
        block={'index':len(self.chain)+1,
               'timestamp':str(datetime.datetime.now()),
               'proof':proof,
               'prev_hash':prev_hash}
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
     return self.chain[-1]
    
    def get_prev_hash(self):
        return self.chain[-1]
    
    def proof_of_work(self, prev_proof):
        new_proof=1
        check_proof=False
        while check_proof is False:
            hash_operation=hashlib.sha256(str(new_proof**2-prev_proof**2).encode()).hexdigest()
            if hash_operation[:4]=='0000':
                check_proof=True
            else:
                new_proof+=1
        return new_proof


    def hash(self, block):
        encoded_block=json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self,chain):
        prev_block=chain[0]
        block_index=1
        while block_index<len(chain):
            block=chain[block_index]
            if block['prev_hash']!=self.hash(prev_block):
                return False
            prev_proof=prev_block['proof']
            proof=block['proof']
            hash_operation=hashlib.sha256(str(proof**2-prev_proof**2).encode()).hexdigest()
            if hash_operation[:4]!='0000':
                return False
            prev_block=block
            block_index+=1
        return True
    
# Mining our blockchain

# Using flask framework for the web app
app = Flask(__name__)

# Creating blockchain instance
Blockchain = Blockchain()

# Mining new block
@app.route('/mine_block',methods=['GET'])

def mine_block():
    prev_block=Blockchain.get_previous_block()
    prev_proof=prev_block['proof']
    proof=Blockchain.proof_of_work(prev_proof)
    prev_hash=Blockchain.hash(prev_block)
    block=Blockchain.create_block(proof, prev_hash)
    responce={
        'message':"Congratulations!",
        'index':block['index'],
        'timestamp':block['timestamp'],
        'proof':block['proof'],
        'prev_hash':block['prev_hash']
        }
    return jsonify(responce),200

@app.route('/get_chain',methods=['GET'])

def get_chain():
    responce={'chain':Blockchain.chain,
              'length':len(Blockchain.chain)}
    return jsonify(responce),200



# Running the app
app.run(host='0.0.0.0',port=5000)