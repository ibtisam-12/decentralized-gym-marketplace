import hashlib
import json
from datetime import datetime, timezone
import os

class Blockchain:
    def __init__(self, data_file=None):
        self.chain = []
        self.blockchain_file = data_file or os.environ.get('BLOCKCHAIN_DATA_FILE', 'blockchain_data.json')
        self.load_blockchain()
        if not self.chain:
            self.create_genesis_block()

    def load_blockchain(self):
        try:
            if os.path.exists(self.blockchain_file):
                with open(self.blockchain_file, 'r') as f:
                    loaded_chain = json.load(f)
                    if isinstance(loaded_chain, list) and len(loaded_chain) > 0:
                        self.chain = loaded_chain
                    else:
                        self.chain = []
        except (FileNotFoundError, json.JSONDecodeError):
            self.chain = []

    def save_blockchain(self):
        try:
            with open(self.blockchain_file, 'w') as f:
                json.dump(self.chain, f, indent=4)
        except (IOError, OSError) as e:
            print(f"Error saving blockchain: {str(e)}")

    def create_genesis_block(self):
        if not self.chain:
            genesis_block = {
                'index': 1,
                'timestamp': str(datetime.now(timezone.utc)),
                'data': "Genesis Block",
                'previous_hash': "0",
            }
            genesis_block['hash'] = self._hash_block(genesis_block)
            self.chain.append(genesis_block)
            self.save_blockchain()

    def create_block(self, data, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.now(timezone.utc)),
            'data': data,
            'previous_hash': previous_hash,
        }
        block['hash'] = self._hash_block(block)
        self.chain.append(block)
        self.save_blockchain()
        return block
    
    def get_last_block(self):
        return self.chain[-1] if self.chain else None

    def _hash_block(self, block):
        block_copy = block.copy()
        if 'hash' in block_copy:
            del block_copy['hash']
        block_string = json.dumps(block_copy, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def add_block(self, data):
        try:
            last_block = self.get_last_block()
            previous_hash = last_block['hash'] if last_block else "0"
            return self.create_block(data, previous_hash)
        except Exception as e:
            print(f"Error adding block: {str(e)}")
            raise

_blockchain_instance = None

def get_blockchain():
    global _blockchain_instance
    if _blockchain_instance is None:
        _blockchain_instance = Blockchain()
    return _blockchain_instance
