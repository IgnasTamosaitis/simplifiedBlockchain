import time
from typing import List, Optional
from hash_utils import my_hash
from models.transaction import Transaction
from models.merkle_tree import MerkleTree


class BlockHeader:
    """Represents a block header containing metadata."""
    
    def __init__(
        self,
        version: int,
        index: int,
        prev_block_hash: str,
        merkle_root: str,
        timestamp: int,
        difficulty_target: str,
        nonce: int = 0,
    ):
        """
        Initialize block header.
        
        Args:
            version: Blockchain version
            index: Block index in chain
            prev_block_hash: Hash of previous block
            merkle_root: Merkle root of transactions
            timestamp: Block creation timestamp
            difficulty_target: Mining difficulty (e.g., "000")
            nonce: Proof-of-work nonce
        """
        self.version = version
        self.index = index
        self.prev_block_hash = prev_block_hash
        self.merkle_root = merkle_root
        self.timestamp = timestamp
        self.difficulty_target = difficulty_target
        self.nonce = nonce
    
    def to_string(self) -> str:
        """
        Convert header to string for hashing.
        """
        return (
            str(self.version) +
            str(self.index) +
            self.prev_block_hash +
            self.merkle_root +
            str(self.timestamp) +
            self.difficulty_target +
            str(self.nonce)
        )
    
    def __repr__(self) -> str:
        return (
            f"BlockHeader(index={self.index}, "
            f"prev={self.prev_block_hash[:8]}..., "
            f"merkle={self.merkle_root[:8]}..., "
            f"nonce={self.nonce})"
        )


class Block:
    """Represents a block in the blockchain."""
    
    def __init__(self, header: BlockHeader, transactions: List[Transaction]):
        """
        Initialize a block.
        
        Args:
            header: Block header
            transactions: List of transactions in this block
        """
        self.header = header
        self.transactions = transactions
        self.index = header.index
        
        # Build Merkle Tree
        self.merkle_tree = self._build_merkle_tree()
    
    def _build_merkle_tree(self) -> MerkleTree:
        """
        Build Merkle Tree from transactions.
        """
        tx_ids = [tx.tx_id for tx in self.transactions]
        return MerkleTree(tx_ids)
    
    def get_merkle_root(self) -> str:
        """
        Get the Merkle root hash.
        """
        return self.merkle_tree.get_root()
    
    def get_hash(self) -> str:
        """
        Calculate and return the block hash.
        """
        header_string = self.header.to_string()
        return my_hash(header_string)
    
    def mine(self) -> str:
        """
        Mine the block by finding a valid nonce.
        """
        target = self.header.difficulty_target
        
        print(f"[MINING] Mining block #{self.index}...")
        print(f"[MINING] Target: hash must start with '{target}'")
        
        attempts = 0
        while True:
            block_hash = self.get_hash()
            
            if block_hash.startswith(target):
                print(f"[MINING] Success! Nonce: {self.header.nonce}, Attempts: {attempts}")
                return block_hash
            
            self.header.nonce += 1
            attempts += 1
            
            # Progress indicator
            if attempts % 50000 == 0:
                print(f"[MINING] Attempt {attempts}... Hash: {block_hash[:16]}...")
    
    @staticmethod
    def build(
        index: int,
        prev_block_hash: str,
        version: int,
        transactions: List[Transaction],
        difficulty_target: str,
        timestamp: Optional[int] = None,
    ) -> "Block":
        """
        Build a new block with proper Merkle root.
        
        Args:
            index: Block index
            prev_block_hash: Previous block hash
            version: Blockchain version
            transactions: List of transactions
            difficulty_target: Mining difficulty
            timestamp: Block timestamp (default: current time)
            
        Returns:
            New Block instance
        """
        if timestamp is None:
            timestamp = int(time.time())
        
        # Build temporary block to get Merkle root
        temp_header = BlockHeader(
            version=version,
            index=index,
            prev_block_hash=prev_block_hash,
            merkle_root="0" * 64,  # Temporary
            timestamp=timestamp,
            difficulty_target=difficulty_target,
            nonce=0,
        )
        temp_block = Block(temp_header, transactions)
        
        # Get real Merkle root
        merkle_root = temp_block.get_merkle_root()
        
        # Create final header with real Merkle root
        header = BlockHeader(
            version=version,
            index=index,
            prev_block_hash=prev_block_hash,
            merkle_root=merkle_root,
            timestamp=timestamp,
            difficulty_target=difficulty_target,
            nonce=0,
        )
        
        return Block(header, transactions)
    
    def __repr__(self) -> str:
        return (
            f"Block(index={self.index}, "
            f"hash={self.get_hash()[:16]}..., "
            f"txs={len(self.transactions)})"
        )