from datetime import datetime
import hashlib
from json import dumps as jdumps


class Block:
    def __init__(self, index, proof, prev_hash, data=''):
        self.index = index
        self.timestamp = str(datetime.now())
        self.proof = proof
        self.prev_hash = prev_hash
        self.data = data
        self.data = data

    def json_default(self):
        try:
            return self.__dict__
        except AttributeError:
            raise TypeError(
                "{} can not be JSON encoded".format(
                    type(self)
                )
            )

    def gen_hash(self):
        encoded_json = jdumps(self.json_default(),
                               sort_keys=True
                               ).encode()
        return hashlib.sha256(encoded_json).hexdigest()


class Blockchain:

    def __init__(self):
        self.chain = []
        self.create_block(proof=1, prev_hash='0')

    def create_block(self, proof, prev_hash, data='') -> Block:
        index = len(self.chain) + 1
        block = Block(index, proof, prev_hash)
        self.chain.append(block)
        return block

    def get_prev_block(self) -> Block:
        return self.chain[-1]

    def proof_of_work(self, prev_proof):
        new_proof = 1
        check_proof = False
        while not check_proof:
            worked_hash = self.do_work(new_proof, prev_proof)
            if worked_hash[:4] == '0000':
                check_proof == True
                # break
                return new_proof
            else:
                new_proof += 1
        # return hashlib.sha256(
        #     str(new_proof**2 - prev_proof**2).encode(

        #     )
        # ).hexdigest()

    @staticmethod
    def do_work(new_proof, prev_proof):
        worked_hash = hashlib.sha256(
            str(new_proof**2 - prev_proof**2).encode(
            )
        ).hexdigest()
        return worked_hash


    def is_valid(self) -> bool:
        chain = self.chain
        prev_block = chain[0]
        block_index = 1
        chain_len = len(chain)
        while block_index < chain_len:
            block_nw = chain[block_index]
            if block_nw.prev_hash != prev_block.gen_hash():
                return False
            prev_proof = prev_block.proof
            proof_nw = block_nw.proof
            worked_hash = self.do_work(proof_nw, prev_proof)
            if worked_hash[:4] != '0000':
                return False
            prev_block = block_nw
            block_index += 1
        return True

