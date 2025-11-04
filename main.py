from models.blockchain import Blockchain


def main():
    """Run the blockchain simulation."""
    print("=" * 60)
    print("BLOCKCHAIN v0.2 - Simplified Implementation")
    print("=" * 60)
    print()
    
    # Initialize blockchain with EASY difficulty
    blockchain = Blockchain(difficulty_target="0")
    
    # Generate users
    blockchain.generate_users(n=100)
    
    # Generate transactions
    blockchain.generate_transactions(m=500)
    
    # Mine all blocks competitively
    blockchain.mine_until_done(block_tx_count=50)
    
    # Print summary
    print(blockchain.summary())


if __name__ == "__main__":
    main()