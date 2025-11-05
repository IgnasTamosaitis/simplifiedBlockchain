from models.blockchain import Blockchain


def main():
    """Run the blockchain simulation."""
    print("=" * 60)
    print("BLOCKCHAIN v0.2")
    print("=" * 60)
    print()
    
    # Initialize blockchain with difficulty "000" (3 zeros - task requirement)
    blockchain = Blockchain(difficulty_target="000")
    
    # Generate users
    blockchain.generate_users(n=1000)
    
    # Generate transactions
    blockchain.generate_transactions(m=10000)
    
    # Mine all blocks competitively
    blockchain.mine_until_done(block_tx_count=100)
    
    # Print summary
    print(blockchain.summary())


if __name__ == "__main__":
    main()