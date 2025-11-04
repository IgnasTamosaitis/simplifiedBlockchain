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
        print(f"[INIT] Difficulty target: '{self.difficulty_target}'")

        genesis_block = Block.build(
            index=0,
            prev_block_hash="0" * 64,
            version=self.version,
            transactions=[],
            difficulty_target=self.difficulty_target,
            timestamp=int(time.time()),
        )
        
        # Try mining with attempt limit, accept any hash if limit reached
        print("[MINING] Attempting to mine genesis block...")
        max_attempts = 500000
        for attempt in range(1, max_attempts + 1):
            genesis_block.header.nonce += 1
            block_hash = genesis_block.get_hash()
            
            if attempt % 50000 == 0:
                print(f"[MINING] Attempt {attempt}... Hash: {block_hash[:16]}...")
            
            if block_hash.startswith(self.difficulty_target):
                print(f"[OK] Valid genesis block found at attempt {attempt}!")
                break
        else:
            # Fallback: accept best hash after max attempts
            print(f"[FALLBACK] No valid hash found in {max_attempts} attempts")
            print(f"[FALLBACK] Accepting genesis block with hash: {block_hash[:16]}...")

        self.chain.append(genesis_block)

        print("[OK] Genesis blokas sukurtas!")
        print(f"     Hash: {block_hash[:32]}...")
        print(f"     Merkle Root: {genesis_block.get_merkle_root()[:32]}...")
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
        print(f"\n{'='*60}")
        print(f"📝 TRANSAKCIJŲ GENERAVIMAS")
        print(f"{'='*60}")
        print(f"Generuojama transakcijų: {m}")
        print()

        keys = list(self.users.keys())
        valid_count = 0
        invalid_count = 0
        
        # Show first 5 transactions in detail
        show_details = 5
        
        for i in range(m):
            sender_key, receiver_key = random.sample(keys, 2)
            sender = self.users[sender_key]
            receiver = self.users[receiver_key]
            
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
            is_valid = self.validate_transaction(tx)
            
            # Show details for first few transactions
            if i < show_details:
                status = "✅ VALID" if is_valid else "❌ INVALID"
                print(f"Transaction #{i+1} {status}")
                print(f"  ID:       {tx.tx_id[:16]}...")
                print(f"  From:     {sender.name} ({sender_key[:8]}...)")
                print(f"  To:       {receiver.name} ({receiver_key[:8]}...)")
                print(f"  Amount:   {amount}")
                print(f"  Balance:  {sender.balance}")
                print(f"  Hash:     {tx.get_hash()[:32]}...")
                print(f"  Time:     {tx.timestamp}")
                print()
            
            if is_valid:
                self.pending_transactions.append(tx)
                valid_count += 1
            else:
                invalid_count += 1

        print(f"{'='*60}")
        print(f"📊 TRANSAKCIJŲ STATISTIKA")
        print(f"{'='*60}")
        print(f"✅ Validžios transakcijos:  {valid_count}")
        print(f"❌ Atmestos transakcijos:   {invalid_count}")
        print(f"📦 Transakcijų fonde:       {len(self.pending_transactions)}")
        print(f"{'='*60}\n")

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
        
        print(f"\n[POOL] Kuriami kandidatiniai blokai ({self.mining_pool.num_candidates} vnt)...")
        
        # Create candidate blocks
        candidates = self.mining_pool.create_candidates(
            all_transactions=self.pending_transactions,
            prev_block_hash=prev_block_hash,
            index=len(self.chain),
            version=self.version,
            difficulty_target=self.difficulty_target,
            tx_per_block=tx_count,
        )
        
        print(f"[MINING] Pradedamas konkurencinis kasimas...\n")
        
        # Mine competitively with faster fallback parameters
        winner = self.mining_pool.mine_competitively(
            candidates=candidates,
            time_limit=3.0,  # Start with 3s per round
            max_attempts_per_round=150000,  # 30k per candidate
        )
        
        if winner:
            return winner.block
        else:
            return None

    def apply_block_state_changes(self, block: Block) -> None:
        """
        Apply state changes from a mined block.
        Only applies valid transactions (balance check at execution time).
        
        Args:
            block: Block to apply
        """
        applied_count = 0
        skipped_count = 0
        
        for tx in block.transactions:
            sender = self.users[tx.sender_key]
            receiver = self.users[tx.receiver_key]
            
            # Re-check balance at execution time (may have changed since validation)
            if sender.balance >= tx.amount:
                sender.debit(tx.amount)
                receiver.credit(tx.amount)
                applied_count += 1
            else:
                # Skip transaction if insufficient balance at execution time
                skipped_count += 1
                print(f"[SKIP] Transaction {tx.tx_id[:8]}... skipped (insufficient balance at execution)")

        if skipped_count > 0:
            print(f"[INFO] Applied {applied_count} transactions, skipped {skipped_count} (insufficient balance)")

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
        
        # Display block like Bitcoin Block Explorer
        self._display_block_info(block)
    
    def _display_block_info(self, block: Block) -> None:
        """Display block information in Bitcoin Block Explorer style."""
        print(f"\n{'='*60}")
        print(f"🧱 BLOCK #{block.index}")
        print(f"{'='*60}")
        print(f"Hash:              {block.get_hash()}")
        print(f"Previous Hash:     {block.header.prev_block_hash[:32]}...")
        print(f"Merkle Root:       {block.get_merkle_root()}")
        print(f"Timestamp:         {block.header.timestamp}")
        print(f"Difficulty Target: {block.header.difficulty_target}")
        print(f"Nonce:             {block.header.nonce}")
        print(f"Transactions:      {len(block.transactions)}")
        print(f"{'='*60}")
        
        # Show first 3 transactions
        if block.transactions:
            print(f"\n📜 TRANSACTIONS (showing first 3 of {len(block.transactions)}):")
            print(f"{'-'*60}")
            for i, tx in enumerate(block.transactions[:3]):
                sender = self.users.get(tx.sender_key)
                receiver = self.users.get(tx.receiver_key)
                print(f"\nTx #{i+1}: {tx.tx_id[:16]}...")
                print(f"  From:   {sender.name if sender else 'Unknown'} → {tx.amount}")
                print(f"  To:     {receiver.name if receiver else 'Unknown'}")
                print(f"  Hash:   {tx.get_hash()[:32]}...")
            print(f"\n{'-'*60}")
        
        print()

    def mine_until_done(self, block_tx_count: int = 100):
        """
        Mine all pending transactions using competitive mining.
        
        Args:
            block_tx_count: Number of transactions per block
        """
        while len(self.pending_transactions) > 0:
            print("=" * 60)
            print(f"[INFO] Grandinės ilgis: {len(self.chain)} blokų")
            print(f"[INFO] Laukiančių transakcijų: {len(self.pending_transactions)}")

            new_block = self.mine_block_competitively(block_tx_count)
            
            if not new_block:
                print("[ERROR] Kasimas nepavyko!")
                break

            self.apply_block_state_changes(new_block)
            self.add_block_to_chain(new_block)
            
            print(f"✅ Liko neapdorotų transakcijų: {len(self.pending_transactions)}\n")

        # Final summary
        print("\n" + "=" * 60)
        print("🎉 BLOCKCHAIN SUMMARY")
        print("=" * 60)
        print(f"📊 Blokų skaičius:          {len(self.chain)}")
        print(f"👥 Vartotojų skaičius:      {len(self.users)}")
        print(f"📝 Apdorotų transakcijų:    {sum(len(b.transactions) for b in self.chain)}")
        print(f"⏱️  Genesis timestamp:       {self.chain[0].header.timestamp}")
        print(f"⏱️  Last block timestamp:    {self.chain[-1].header.timestamp}")
        print(f"🔗 Genesis hash:            {self.chain[0].get_hash()[:32]}...")
        print(f"🔗 Last block hash:         {self.chain[-1].get_hash()[:32]}...")
        print(f"🌳 Last Merkle root:        {self.chain[-1].get_merkle_root()[:32]}...")
        print("=" * 60 + "\n")

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