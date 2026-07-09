import json
import tempfile
import os
from django.test import TestCase
from blockchain.utils import Blockchain

class BlockchainTests(TestCase):
    def setUp(self):
        self.tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json', mode='w')
        self.tmp_file.close()

    def tearDown(self):
        if os.path.exists(self.tmp_file.name):
            os.unlink(self.tmp_file.name)

    def test_genesis_block_created_on_init(self):
        bc = Blockchain(data_file=self.tmp_file.name)
        self.assertEqual(len(bc.chain), 1)
        self.assertEqual(bc.chain[0]['index'], 1)
        self.assertEqual(bc.chain[0]['previous_hash'], '0')
        self.assertIn('hash', bc.chain[0])

    def test_add_block_extends_chain(self):
        bc = Blockchain(data_file=self.tmp_file.name)
        data = {'action': 'test', 'user': 'admin'}
        block = bc.add_block(data)
        self.assertEqual(len(bc.chain), 2)
        self.assertEqual(block['index'], 2)
        self.assertEqual(block['data'], data)

    def test_blocks_are_chained(self):
        bc = Blockchain(data_file=self.tmp_file.name)
        first = bc.add_block({'action': 'first'})
        second = bc.add_block({'action': 'second'})
        self.assertEqual(second['previous_hash'], first['hash'])

    def test_hash_changes_when_data_changes(self):
        bc = Blockchain(data_file=self.tmp_file.name)
        bc.add_block({'action': 'original'})
        original_hash = bc.chain[1]['hash']
        bc.chain[1]['data'] = {'action': 'tampered'}
        recalculated = bc._hash_block(bc.chain[1])
        self.assertNotEqual(recalculated, original_hash)

    def test_get_last_block_returns_tip(self):
        bc = Blockchain(data_file=self.tmp_file.name)
        self.assertEqual(bc.get_last_block()['index'], 1)
        bc.add_block({'action': 'test'})
        self.assertEqual(bc.get_last_block()['index'], 2)

    def test_chain_persistence(self):
        bc = Blockchain(data_file=self.tmp_file.name)
        bc.add_block({'action': 'persist_test'})
        del bc
        bc2 = Blockchain(data_file=self.tmp_file.name)
        self.assertEqual(len(bc2.chain), 2)
        self.assertEqual(bc2.chain[1]['data']['action'], 'persist_test')
