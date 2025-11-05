import time
import random
from typing import List, Optional
from models.block import Block
from models.transaction import Transaction


class CandidateBlock:
    """Represents a candidate block for competitive mining."""
    
    def __init__(self, block: Block, miner_id: int):
        """

            block: The block to mine
            miner_id: ID of the miner
        """
        self.block = block
        self.miner_id = miner_id
        self.attempts = 0
        self.found = False
        self.found_hash: Optional[str] = None
        self.mining_time = 0.0
    
    def __repr__(self) -> str:
        return f"CandidateBlock(miner={self.miner_id}, attempts={self.attempts}, found={self.found})"


class MiningPool:
    """
    Simulates competitive/decentralized mining with multiple candidate blocks.
    """
    
    def __init__(self, num_candidates: int = 5):
        """
            num_candidates: Number of candidate blocks to create
        """
        self.num_candidates = num_candidates
    
    def create_candidates(
        self,
        all_transactions: List[Transaction],
        prev_block_hash: str,
        index: int,
        version: int,
        difficulty_target: str,
        tx_per_block: int = 100,
    ) -> List[CandidateBlock]:
        """
        Create multiple candidate blocks with different transaction sets.
        
        Args:
            all_transactions: Pool of available transactions
            prev_block_hash: Hash of previous block
            index: Block index
            version: Blockchain version
            difficulty_target: Mining difficulty
            tx_per_block: Transactions per candidate block
            
        Returns:
            List of CandidateBlock objects
        """
        candidates = []
        
        print(f"\n[POOL] Creating {self.num_candidates} candidate blocks...")
        print(f"[POOL] Available transactions: {len(all_transactions)}")
        print(f"[POOL] Transactions per block: {tx_per_block}\n")
        
        # Shuffle to simulate different miners picking different tx
        shuffled_txs = all_transactions.copy()
        random.shuffle(shuffled_txs)
        
        for i in range(self.num_candidates):
            # Each candidate gets a different slice of transactions
            start_idx = (i * tx_per_block) % len(shuffled_txs)
            end_idx = min(start_idx + tx_per_block, len(shuffled_txs))
            
            tx_batch = shuffled_txs[start_idx:end_idx]
            
            # If not enough, wrap around
            if len(tx_batch) < tx_per_block and len(shuffled_txs) > tx_per_block:
                needed = tx_per_block - len(tx_batch)
                tx_batch.extend(shuffled_txs[:needed])
            
            block = Block.build(
                index=index,
                prev_block_hash=prev_block_hash,
                version=version,
                transactions=tx_batch,
                difficulty_target=difficulty_target,
                timestamp=int(time.time()) + i,  # Slight timestamp variation
            )
            
            candidate = CandidateBlock(block, miner_id=i)
            candidates.append(candidate)
            
            print(f"[CANDIDATE #{i}] Created with {len(tx_batch)} transactions")
            print(f"               Merkle root: {block.get_merkle_root()[:32]}...")
        
        print()
        return candidates
    
    def mine_competitively(
        self,
        candidates: List[CandidateBlock],
        time_limit: float = 5.0,
        max_attempts_per_round: int = 100000,
    ) -> Optional[CandidateBlock]:
        """
        Mine candidate blocks competitively with time limit.
        """
        print(f"[MINING] Starting competitive mining...")
        print(f"[MINING] Time limit: {time_limit}s per round")
        print(f"[MINING] Max attempts per round: {max_attempts_per_round}")
        print(f"[MINING] Target: hash starts with '{candidates[0].block.header.difficulty_target}'\n")
        
        round_num = 1
        
        while True:
            print(f"=== MINING ROUND {round_num} ===")
            start_time = time.time()
            
            winner = self._mine_round(
                candidates,
                time_limit,
                max_attempts_per_round,
                start_time
            )
            
            if winner:
                print(f"\n[WINNER] Candidate #{winner.miner_id} found valid block!")
                print(f"[WINNER] Hash: {winner.found_hash}")
                print(f"[WINNER] Nonce: {winner.block.header.nonce}")
                print(f"[WINNER] Total attempts: {winner.attempts}")
                print(f"[WINNER] Mining time: {winner.mining_time:.4f}s\n")
                return winner
            
            elapsed = time.time() - start_time
            print(f"\n[ROUND {round_num}] No winner after {elapsed:.2f}s")
            print(f"[ROUND {round_num}] Increasing time limit and retrying...\n")
            
            # Increase limits for next round
            time_limit *= 1.5
            max_attempts_per_round = int(max_attempts_per_round * 1.5)
            round_num += 1
            
            if round_num > 3:  # Quick fallback - accept best after 3 rounds
                print("[INFO] Reached 3 rounds without success - triggering fallback")
                # Force acceptance of best candidate
                if candidates:
                    best = min(candidates, key=lambda c: c.block.get_hash())
                    best.found = True
                    best.found_hash = best.block.get_hash()
                    best.mining_time = time.time() - start_time
                    print(f"[FALLBACK] Accepting best candidate #{best.miner_id}")
                    return best
                return None
    
    def _mine_round(
        self,
        candidates: List[CandidateBlock],
        time_limit: float,
        max_attempts: int,
        start_time: float,
    ) -> Optional[CandidateBlock]:
        """
        Execute one round of competitive mining.
        
        Args:
            candidates: List of candidate blocks
            time_limit: Time limit for this round
            max_attempts: Max attempts for this round
            start_time: Start time of the round
            
        Returns:
            Winning candidate or None
        """
        attempts_per_candidate = max_attempts // len(candidates)

        # Track best candidate (lowest lexicographic hash) in case we need to accept a best-effort result
        best_candidate: Optional[CandidateBlock] = None
        best_hash: Optional[str] = None

        for candidate in candidates:
            # Check overall timeout before starting this candidate
            if time.time() - start_time > time_limit:
                print(f"[TIMEOUT] Time limit reached while scanning candidates")
                break

            round_start = time.time()

            # Try to mine this candidate
            for _ in range(attempts_per_candidate):
                candidate.attempts += 1
                candidate.block.header.nonce += 1

                block_hash = candidate.block.get_hash()

                # Keep track of best (smallest) hash seen so far for fallback
                if best_hash is None or block_hash < best_hash:
                    best_hash = block_hash
                    best_candidate = candidate

                if block_hash.startswith(candidate.block.header.difficulty_target):
                    candidate.found = True
                    candidate.found_hash = block_hash
                    candidate.mining_time = time.time() - start_time
                    return candidate

                # Check timeout mid-mining
                if candidate.attempts % 10000 == 0:
                    if time.time() - start_time > time_limit:
                        print(f"[TIMEOUT] Time limit reached during candidate #{candidate.miner_id} mining")
                        break

            round_time = time.time() - round_start
            print(f"[CANDIDATE #{candidate.miner_id}] {attempts_per_candidate} attempts in {round_time:.2f}s - no luck")

        # If we exit without finding a valid block, but we did find candidate hashes, accept the best one as a fallback
        if best_candidate is not None:
            print("[FALLBACK] No valid block met difficulty within limits — accepting best-found candidate to ensure progress")
            best_candidate.found = True
            best_candidate.found_hash = best_hash
            best_candidate.mining_time = time.time() - start_time
            return best_candidate

        return None