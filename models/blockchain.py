import random
import time
import uuid
from typing import List, Dict, Optional

from hash_utils import my_hash
from models.user import User
from models.transaction import Transaction
from models.block import Block
from models.mining_pool import MiningPool


class Blockchain:
    """Main blockchain class managing the entire blockchain system."""
    
    def __init__(self, difficulty_target: str = "000"):
        """
        Initialize blockchain.
        
        Args:
            difficulty_target: Mining difficulty (e.g., "000" means hash must start with 000)
        """
        self.users: Dict[str, User] = {}
        self.pending_transactions: List[Transaction] = []
        self.chain: List[Block] = []

        self.version = 1
        self.difficulty_target = difficulty_target
        
        # Mining pool for competitive mining
        self.mining_pool = MiningPool(num_candidates=5)

        self._create_genesis_block()

    def _create_genesis_block(self) -> None:
        """Create the genesis (first) block."""
        print("[INIT] Kuriamas GENESIS blokas...")

        genesis_block = Block.build(
            index=0,
            prev_block_hash="0" * 64,
            version=self.version,
            transactions=[],
            difficulty_target=self.difficulty_target,
            timestamp=int(time.time()),
        )
        
        _ = genesis_block.mine()

        self.chain.append(genesis_block)

        print("[OK] Genesis blokas paruoštas.")
        print(f"     Hash: {genesis_block.get_hash()}")
        print(f"     Merkle Root: {genesis_block.get_merkle_root()}")
        print(f"     Nonce: {genesis_block.header.nonce}\n")

    def generate_users(self, n: int = 1000):
        """
        Generate random users.
        
        Args:
            n: Number of users to generate
        """
        print(f"[INFO] Generuojami {n} vartotojai...")

        for _ in range(n):
            name = f"User_{uuid.uuid4().hex[:6]}"
            public_key = uuid.uuid4().hex
            balance = random.randint(100, 1_000_000)

            self.users[public_key] = User(
                name=name,
                public_key=public_key,
                balance=balance,
            )

        print(f"[OK] Sugeneruota {len(self.users)} vartotojų.\n")

    def validate_transaction(self, tx: Transaction) -> bool:
        """
        Validate a transaction before adding to pending pool.
        
        Args:
            tx: Transaction to validate
            
        Returns:
            True if valid, False otherwise
        """
        # Check hash integrity
        if not tx.verify_hash():
            return False
        
        # Check sender exists
        if tx.sender_key not in self.users:
            print(f"[VERIFY] Transaction {tx.tx_id[:8]} - sender not found!")
            return False
        
        # Check receiver exists
        if tx.receiver_key not in self.users:
            print(f"[VERIFY] Transaction {tx.tx_id[:8]} - receiver not found!")
            return False
        
        # Check balance
        sender = self.users[tx.sender_key]
        if not tx.verify_balance(sender.balance):
            return False
        
        return True

    def generate_transactions(self, m: int = 10000):
        """
        Generate random transactions with validation.
        
        Args:
            m: Number of transactions to generate
        """
        print(f"[INFO] Generuojamos {m} transakcijos...")

        keys = list(self.users.keys())
        valid_count = 0
        invalid_count = 0
        
        for _ in range(m):
            sender_key, receiver_key = random.sample(keys, 2)
            sender = self.users[sender_key]
            
            # Generate amount (sometimes intentionally too high to test validation)
            if random.random() < 0.95:  # 95% valid transactions
                amount = random.randint(1, min(5000, sender.balance))
            else:  # 5% invalid (insufficient balance)
                amount = sender.balance + random.randint(1, 1000)

            tx = Transaction(
                sender_key=sender_key,
                receiver_key=receiver_key,
                amount=amount,
            )
            
            # Validate before adding
            if self.validate_transaction(tx):
                self.pending_transactions.append(tx)
                valid_count += 1
            else:
                invalid_count += 1

        print(f"[OK] Valid transactions: {valid_count}")
        print(f"[OK] Invalid (rejected): {invalid_count}")
        print(f"[OK] Total in pool: {len(self.pending_transactions)}\n")

    def pick_transactions_for_block(self, k: int = 100) -> List[Transaction]:
        """
        Pick transactions for a block.
        
        Args:
            k: Number of transactions to pick
            
        Returns:
            List of transactions
        """
        return self.pending_transactions[:k]

    def mine_block_competitively(self, tx_count: int = 100) -> Optional[Block]:
        """
        Mine a block using competitive mining with multiple candidates.
        
        Args:
            tx_count: Number of transactions per candidate block
            
        Returns:
            Mined block or None if mining failed
        """
        if len(self.pending_transactions) < tx_count:
            tx_count = len(self.pending_transactions)
        
        if tx_count == 0:
            return None
        
        prev_block_hash = self.chain[-1].get_hash()
        
        # Create candidate blocks
        candidates = self.mining_pool.create_candidates(
            all_transactions=self.pending_transactions,
            prev_block_hash=prev_block_hash,
            index=len(self.chain),
            version=self.version,
            difficulty_target=self.difficulty_target,
            tx_per_block=tx_count,
        )
        
        # Mine competitively
        winner = self.mining_pool.mine_competitively(
            candidates=candidates,
            time_limit=5.0,
            max_attempts_per_round=100000,
        )
        
        if winner:
            return winner.block
        else:
            return None

    def apply_block_state_changes(self, block: Block) -> None:
        """
        Apply state changes from a mined block.
        
        Args:
            block: Block to apply
        """
        for tx in block.transactions:
            sender = self.users[tx.sender_key]
            receiver = self.users[tx.receiver_key]
            sender.debit(tx.amount)
            receiver.credit(tx.amount)

        used_ids = {t.tx_id for t in block.transactions}
        self.pending_transactions = [
            t for t in self.pending_transactions if t.tx_id not in used_ids
        ]

    def add_block_to_chain(self, block: Block) -> None:
        """
        Add a mined block to the chain.
        
        Args:
            block: Block to add
        """
        self.chain.append(block)

    def mine_until_done(self, block_tx_count: int = 100):
        """
        Mine all pending transactions using competitive mining.
        
        Args:
            block_tx_count: Number of transactions per block
        """
        while len(self.pending_transactions) > 0:
            print("=" * 60)
            print(f"[INFO] Grandinės ilgis dabar: {len(self.chain)} blokai (-as)")
            print(f"[INFO] Liko neapdorotų transakcijų: {len(self.pending_transactions)}\n")

            new_block = self.mine_block_competitively(block_tx_count)
            
            if not new_block:
                print("[ERROR] Mining failed, stopping...")
                break

            self.apply_block_state_changes(new_block)
            self.add_block_to_chain(new_block)

            print(f"[CHAIN] Naujas blokas #{new_block.index} įtrauktas į grandinę.")
            print(f"[CHAIN] Bloko hash: {new_block.get_hash()}")
            print(f"[CHAIN] Merkle root: {new_block.get_merkle_root()}")
            print(f"[CHAIN] Likusios transakcijos: {len(self.pending_transactions)}\n")

        print("=== Viskas baigta ===")
        print(f"Galutinis blokų kiekis: {len(self.chain)}")
        print(f"Vartotojų kiekis:       {len(self.users)}")
        print(f"Paskutinio bloko hash:  {self.chain[-1].get_hash()[:32]}...")
        print("======================\n")

    def summary(self) -> str:
        """
        Get blockchain summary.
        
        Returns:
            Summary string
        """
        return (
            f"Grandinės ilgis: {len(self.chain)} blokai\n"
            f"Vartotojų kiekis: {len(self.users)}\n"
            f"Laukiančių transakcijų: {len(self.pending_transactions)}\n"
            f"Paskutinio bloko hash: {self.chain[-1].get_hash()}\n"
            f"Paskutinio bloko Merkle root: {self.chain[-1].get_merkle_root()}\n"
        )