class User:
    """Represents a user in the blockchain system."""
    
    def __init__(self, name: str, public_key: str, balance: int = 0):
        """
        Initialize a new user.
        Args:
            name: User's display name
            public_key: Unique public key identifier
            balance: Initial balance (default 0)
        """
        self.name = name
        self.public_key = public_key
        self.balance = balance
    
    def credit(self, amount: int) -> None:
        """
        Add funds to user's balance.
        """
        if amount < 0:
            raise ValueError("Cannot credit negative amount")
        self.balance += amount
    
    def debit(self, amount: int) -> None:
        """
        Subtract funds from user's balance.
        """
        if amount < 0:
            raise ValueError("Cannot debit negative amount")
        if amount > self.balance:
            raise ValueError(f"Insufficient balance: has {self.balance}, needs {amount}")
        self.balance -= amount
    
    def __repr__(self) -> str:
        return f"User(name={self.name}, key={self.public_key[:8]}..., balance={self.balance})"