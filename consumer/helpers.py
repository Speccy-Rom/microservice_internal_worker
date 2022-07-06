import hashlib
import time


class PoW:
    MAX_NONCE = 2 ** 32  # 4 billion

    def __init__(self, message, *args, **kwargs):
        self.message = message

    async def proof_of_work(self, header, difficulty_bits):

        # calculate the difficulty target
        target = 2 ** (256 - difficulty_bits)

        for nonce in range(self.MAX_NONCE):
            encode_to_bytes = (str(header) + str(nonce)).encode()
            hash_result = hashlib.sha256(encode_to_bytes).hexdigest()

            # check if this is a valid result, below the target
            if int(hash_result, 16) < target:
                print(("Success with nonce %d" % nonce))
                print(f"Hash is {hash_result}")
                return (hash_result, nonce)

        print(("Failed after %d (max_nonce) tries" % nonce))
        return nonce

    async def calculate(self):
        nonce = 0
        hash_result = ''

        # difficulty from 0 to 31 bits
        original_max_range = 24
        test_range = 24
        calculate_start_time = time.time()
        for difficulty_bits in range(test_range):

            difficulty = 2 ** difficulty_bits
            print(("Difficulty: %ld (%d bits)" % (difficulty, difficulty_bits)))

            print("Starting search...")

            # checkpoint the current time
            start_time = time.time()

            # make a new block which includes the hash from the previous block
            # we fake a block of transactions - just a string
            new_block = self.message + hash_result

            # find a valid nonce for the new block
            (hash_result, nonce) = await self.proof_of_work(new_block, difficulty_bits)

            # checkpoint how long it took to find a result
            end_time = time.time()

            elapsed_time = end_time - start_time
            print(("Elapsed Time: %.4f seconds" % elapsed_time))

            if elapsed_time > 0:
                # estimate the hashes per second
                hash_power = float(int(nonce) / elapsed_time)
                print(("Hashing Power: %ld hashes per second" % hash_power))

        calculate_elapsed_time = time.time() - calculate_start_time
        return hash_result, calculate_elapsed_time
