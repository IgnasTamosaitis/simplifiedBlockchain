from typing import List, Optional
from hash_utils import my_hash


class MerkleTree:
    """
    Merkle Tree implementation for blockchain transactions.
    Builds a binary tree of hashes from transaction IDs.
    """
    
    def __init__(self, transaction_ids: List[str]):
        """
        Initialize Merkle Tree with transaction IDs.
        
        Args:
            transaction_ids: List of transaction ID strings
        """
        self.transaction_ids = transaction_ids
        self.root: Optional[str] = None
        self.tree_levels: List[List[str]] = []
        
        if transaction_ids:
            self._build_tree()
    
    def _build_tree(self) -> None:
        """Build the Merkle Tree from transaction IDs."""
        if not self.transaction_ids:
            self.root = "0" * 64
            return
        
        # Level 0: Hash each transaction ID
        current_level = [my_hash(tx_id) for tx_id in self.transaction_ids]
        self.tree_levels.append(current_level.copy())
        
        print(f"[MERKLE] Building tree from {len(current_level)} transactions...")
        
        # Build upper levels
        level_num = 1
        while len(current_level) > 1:
            next_level = []
            
            # Process pairs
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                
                # If odd number, duplicate the last hash
                right = current_level[i + 1] if i + 1 < len(current_level) else left
                
                # Combine and hash
                combined = left + right
                parent_hash = my_hash(combined)
                next_level.append(parent_hash)
            
            self.tree_levels.append(next_level.copy())
            print(f"[MERKLE] Level {level_num}: {len(next_level)} nodes")
            
            current_level = next_level
            level_num += 1
        
        self.root = current_level[0]
        print(f"[MERKLE] Root hash: {self.root[:32]}...\n")
    
    def get_root(self) -> str:
        """
        Get the Merkle root hash.
        
        Returns:
            Merkle root hash or "0"*64 if no transactions
        """
        return self.root if self.root else "0" * 64
    
    def verify_transaction(self, tx_id: str, proof: List[tuple]) -> bool:
        """
        Verify a transaction exists in the tree using a Merkle proof.
        
        Args:
            tx_id: Transaction ID to verify
            proof: List of (hash, is_left) tuples forming the proof path
            
        Returns:
            True if transaction is verified, False otherwise
        """
        current_hash = my_hash(tx_id)
        
        for sibling_hash, is_left in proof:
            if is_left:
                combined = sibling_hash + current_hash
            else:
                combined = current_hash + sibling_hash
            
            current_hash = my_hash(combined)
        
        return current_hash == self.root
    
    def get_proof(self, tx_id: str) -> Optional[List[tuple]]:
        """
        Generate Merkle proof for a transaction.
        
        Args:
            tx_id: Transaction ID to generate proof for
            
        Returns:
            List of (hash, is_left) tuples or None if tx not found
        """
        if tx_id not in self.transaction_ids:
            return None
        
        index = self.transaction_ids.index(tx_id)
        proof = []
        
        for level in self.tree_levels[:-1]:  # Exclude root level
            if index % 2 == 0:
                # Current node is left child
                sibling_index = index + 1
                is_left = False
            else:
                # Current node is right child
                sibling_index = index - 1
                is_left = True
            
            if sibling_index < len(level):
                proof.append((level[sibling_index], is_left))
            
            index //= 2
        
        return proof
    
    def __repr__(self) -> str:
        return f"MerkleTree(transactions={len(self.transaction_ids)}, root={self.root[:16] if self.root else 'None'}...)"