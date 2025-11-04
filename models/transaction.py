"""
Transaction klasė reprezentuoja lėšų pervedimą tarp dviejų adresų.

Laukai:
- sender_key: siuntėjo public_key
- receiver_key: gavėjo public_key
- amount: kiek pinigų siunčiama
- timestamp: kada transakcija sukurta (epoch sekundėmis)
- tx_id: transakcijos identifikatorius (maišos reikšmė pagal kitus laukus)

transaction_id = hash(sender, receiver, amount, timestamp)
"""

import time
from hash_utils import my_hash

class Transaction:
    def __init__(self, sender_key: str, receiver_key: str, amount: int):
        self.tx_id = str(uuid.uuid4())
        self.sender_key = sender_key
        self.receiver_key = receiver_key
        self.amount = amount
        self.timestamp = int(time.time())
        
        # Calculate transaction hash
        self._hash = self._calculate_hash()
    
    def _calculate_hash(self) -> str:
        """Calculate the transaction hash."""
        data = (
            self.tx_id +
            self.sender_key +
            self.receiver_key +
            str(self.amount) +
            str(self.timestamp)
        )
        return my_hash(data)
    
    def get_hash(self) -> str:
        """Get the transaction hash."""
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