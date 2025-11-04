"""
Transaction model for blockchain transactions.
"""

import time
import uuid
from hash_utils import my_hash


class Transaction:
    """Represents a transaction between two users."""
    
    def __init__(self, sender_key: str, receiver_key: str, amount: int):
        """
        Initialize a new transaction.
        
        Args:
            sender_key: Public key of sender
            receiver_key: Public key of receiver
            amount: Amount to transfer
        """
        self.tx_id = str(uuid.uuid4())
        self.sender_key = sender_key
        self.receiver_key = receiver_key
        self.amount = amount
        self.timestamp = int(time.time())
        
        # Calculate transaction hash
        self._hash = self._calculate_hash()
    
    def _calculate_hash(self) -> str:
        """
        Calculate the transaction hash.
        
        Returns:
            64-character hex hash string
        """
        data = (
            self.tx_id +
            self.sender_key +
            self.receiver_key +
            str(self.amount) +
            str(self.timestamp)
        )
        return my_hash(data)
    
    def get_hash(self) -> str:
        """
        Get the transaction hash.
        
        Returns:
            Transaction hash
        """
        return self._hash
    
    def verify_hash(self) -> bool:
        """
        Verify that the transaction hash is correct.
        
        Returns:
            True if hash is valid, False otherwise
        """
        recalculated = self._calculate_hash()
        is_valid = recalculated == self._hash
        
        if not is_valid:
            print(f"[VERIFY] Transaction {self.tx_id[:8]} hash INVALID!")
            print(f"         Expected: {self._hash[:32]}...")
            print(f"         Got:      {recalculated[:32]}...")
        
        return is_valid
    
    def verify_balance(self, sender_balance: int) -> bool:
        """
        Verify sender has sufficient balance.
        
        Args:
            sender_balance: Current balance of sender
            
        Returns:
            True if sender has enough balance, False otherwise
        """
        is_valid = sender_balance >= self.amount
        
        if not is_valid:
            print(f"[VERIFY] Transaction {self.tx_id[:8]} INSUFFICIENT BALANCE!")
            print(f"         Sender has: {sender_balance}, needs: {self.amount}")
        
        return is_valid
    
    def __repr__(self) -> str:
        return (
            f"Transaction(id={self.tx_id[:8]}..., "
            f"from={self.sender_key[:8]}..., "
            f"to={self.receiver_key[:8]}..., "
            f"amount={self.amount})"
        )