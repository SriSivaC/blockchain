from blockchain import Block,Blockchain
from json import dumps as jdumps
from flask import Flask, jsonify

app = Flask(__name__)
 # app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
blockchain = Blockchain()

@app.route('/block/mine', methods=['GET'])
def mine_block():
    prev_block = blockchain.get_prev_block()
    prev_proof = prev_block.proof
    proof = blockchain.proof_of_work(prev_proof)
    prev_hash = prev_block.gen_hash()
    block_nw = blockchain.create_block(proof, prev_hash)
    try:
        response = {
            'message': 'Congratulations! You just mined a block!!!',
            'block': block_nw.json_default()
        }
        status = 200
    except Exception as e:
        status = 400
        message = e
        response = {
            'message': message,
            'block': None
        }
    return jdumps(response), status

@app.route('/', methods=['GET'])
def get_chain():
    chain = blockchain.chain
    try:
        response = {
            'chain': chain,
            'length': len(chain)
        }
        status = 200
    except Exception as e:
        status = 400
        message = e
        response = {
            'chain': None,
            'length': None
        }
    return jdumps(response, default=Block.json_default), status

@app.route('/check',methods=['GET'])
def is_valid():
    response = {
        'valid': blockchain.is_valid()
    }
    return jdumps(response)

if __name__ == '__main__':
    app.run(debug=True)
