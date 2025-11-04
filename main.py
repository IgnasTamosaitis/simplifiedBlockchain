from models.blockchain import Blockchain


def main():
    """Run the blockchain simulation."""
    print("=" * 60)
    print("BLOCKCHAIN v0.2 - Simplified Implementation")
    print("=" * 60)
    print()
    
    # Initialize blockchain with difficulty
    blockchain = Blockchain(difficulty_target="00")
    
    # Generate users
    blockchain.generate_users(n=1000)
    
    # Generate transactions (with validation)
    blockchain.generate_transactions(m=10000)
    
    # Mine all blocks competitively
    blockchain.mine_until_done(block_tx_count=100)
    
    # Print summary
    print("\n" + "=" * 60)
    print("FINAL SUMMARY")
    print("=" * 60)
    print(blockchain.summary())


if __name__ == "__main__":
    main()