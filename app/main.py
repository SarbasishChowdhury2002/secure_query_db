'''
from fastapi import FastAPI

app = FastAPI(title="Secure Query Processing over Encrypted & Sharded DBs")

@app.get("/")
def root():
    return {"status": "System running on Windows"}


from app.db.shard1 import insert_user

if __name__ == "__main__":
    insert_user(
        username="alice",
        email="alice@gmail.com",
        password="StrongPassword123"
    )
    print("Encrypted data inserted successfully!")


from app.db.shard2 import insert_user

if __name__ == "__main__":
    insert_user(
        username="bob",
        email="bob@gmail.com",
        password="StrongPassword123"
    )
    print("Encrypted data inserted successfully!")


from app.db.shard3 import insert_user

if __name__ == "__main__":
    insert_user(
        username="candy",
        email="candy@gmail.com",
        password="StrongPassword123"
    )
    print("Encrypted data inserted successfully!")



# week 3 quick test -> crypto/search.py
from app.crypto.search import SearchableEncryption

se = SearchableEncryption(b"week3-secret-key")

print(se.generate_token("salary"))
print(se.generate_trapdoor("salary"))
print(se.generate_and_trapdoor(["salary", "bonus"]))
'''


'''
# week 3 quick test -> secure_query.py
from app.db.secure_query import SecureQueryEngine
from app.db import shard1, shard2, shard3

engine = SecureQueryEngine([shard1, shard2, shard3])

results = engine.and_search(["token_salary", "token_bonus"])
print(results)
'''

'''
#week 3 rbac testing
from app.db.secure_query import SecureQueryEngine
from app.db import shard1, shard2, shard3

engine = SecureQueryEngine([shard1, shard2, shard3])

# Try authorized role
print("Analyst search:")
print(engine.and_search(
    ["token_salary", "token_bonus"],
    user_role="analyst"
))

# Try unauthorized role
print("Guest search:")
print(engine.and_search(
    ["token_salary"],
    user_role="guest"
))
'''

'''
# week 3 secure read + controlled decryption test
from app.db.secure_query import SecureQueryEngine
from app.db import shard1, shard2, shard3

engine = SecureQueryEngine([shard1, shard2, shard3])

print("Admin read:")
print(engine.secure_read(
    ["token_salary", "token_bonus"],
    user_role="admin"
))

print("\nAnalyst read:")
print(engine.secure_read(
    ["token_salary", "token_bonus"],
    user_role="analyst"
))
'''

'''
# week 3 password hashing test
from app.crypto.password_hash import PasswordManager

pm = PasswordManager()

print("\n--- Password Hashing Test ---")

password = "securePassword123"

hashed = pm.hash_password(password)
print("Hashed password:", hashed)

print("Verify correct password:",
      pm.verify_password("securePassword123", hashed))

print("Verify wrong password:",
      pm.verify_password("wrongPassword", hashed))
'''

'''
# week 3 encryption key versioning test
from app.crypto.encrypt import encrypt_data, decrypt_data

print("\n--- Key Version Test ---")

nonce, cipher, version = encrypt_data("Test Message")
print("Key Version:", version)

plaintext = decrypt_data(nonce, cipher, version)
print("Decrypted:", plaintext)
'''

'''
# week 3 key rotation test
from app.crypto.encrypt import key_manager

print("\nCurrent Key Version:", key_manager.current_version)

print("Rotating key...")
key_manager.rotate_key()

print("New Key Version:", key_manager.current_version)
'''

# week 3 secure read + controlled decryption test with shard routing

'''from app.db.secure_query import SecureQueryEngine
engine = SecureQueryEngine()
print("\nUser sarbasish:")
print(engine.secure_read(
    ["token_salary", "token_bonus"],
    user_role="admin",
    user_identifier="sarbasish"
))
print("\nUser kunal:")
print(engine.secure_read(
    ["token_salary", "token_bonus"],
    user_role="admin",
    user_identifier="kunal"
))'''

'''
from app.coordinator.shard_insert_router import ShardInsertRouter

router = ShardInsertRouter()

router.insert_user("sarbasish", "sarbasish", "s@email.com", "pass1")
router.insert_user("kunal", "kunal", "k@email.com", "pass2")
router.insert_user("rohit", "rohit", "r@email.com", "pass3")
'''

'''
from app.coordinator.query_router import ShardRouter

router = ShardRouter()

users = ["sarbasish", "kunal", "rohit"]

for u in users:
    shard = router.route(u)
    print(f"{u} → {shard.__name__}")
'''

import hashlib
import time
from app.crypto.search import SearchableEncryption
from app.db import shard1
from app.db.secure_query import SecureQueryEngine
from app.experiments.benchmark import run_benchmark
from app.utils.logger import log_query
from app.utils.logger import log_query_csv
from app.blockchain.ledger import BlockchainLogger
from app.utils.access_pattern import AccessPatternTracker
from app.experiments.dataset_generator import generate_dataset


from app.experiments.benchmark import run_benchmark
from app.experiments.keyword_benchmark import run_keyword_benchmark
from app.experiments.shard_benchmark import run_shard_benchmark

# ==============================
# CONFIG
# ==============================
#SEARCH_KEY = b"week3-secret-key"
from app.utils.constants import SEARCH_KEY

# ==============================
# MAIN PIPELINE TEST
# ==============================

blockchain = BlockchainLogger()

tracker = AccessPatternTracker()


def run_pipeline():

    print("\n===== SYSTEM TEST: END-TO-END PIPELINE =====\n")

    # --------------------------
    # Step 1: Initialize Search Encryption
    # --------------------------
    se = SearchableEncryption(SEARCH_KEY)

    # --------------------------
    # Step 2: Define Query
    # --------------------------
    user_identifier = "sarbasish"
    user_role = "admin"

    dataset = generate_dataset(1000)   # 1K dataset
    shard1.load_dataset(dataset)

    keywords = ["salary", "bonus"]

    #keywords = ["unknown"] # Testing with a keyword that doesn't exist to show no results case

    '''
    queries = [         # Testing access pattern leakage with repeated queries
        ["salary"],
        ["salary"],
        ["salary", "bonus"],
        ["bonus"],
        ["salary"],
    ]
    '''

    print("User:", user_identifier)
    print("Role:", user_role)
    print("Keywords:", keywords)

    # --------------------------
    # Step 3: Generate Trapdoors
    # --------------------------
    trapdoors = se.generate_and_trapdoor(keywords)

    print("\nTrapdoors:")
    for t in trapdoors:
        print(t)

    # --------------------------
    # Step 4: Execute Secure Query
    # --------------------------

    query_string = f"{user_identifier}:{keywords}"
    query_hash = hashlib.sha256(query_string.encode()).hexdigest()

    engine = SecureQueryEngine()

    start = time.time()

    '''results = engine.secure_read(
        trapdoors=trapdoors,
        user_role=user_role,
        #user_role = "guest",  # Testing with unauthorized role to show access control
        #user_role = "analyst", # Testing with analyst role that has read access but no decryption
        user_identifier=user_identifier
        #user_identifier = "rohit" # Testing with a user that has no relevant data to show empty results case
    )'''

    results, shard_index = engine.secure_read(
        trapdoors=trapdoors,
        user_role=user_role,
        user_identifier=user_identifier
    )


    end = time.time()

    query_time = round(end - start, 6)

    # ✅ LOGGING HERE
    log_query(
        user=user_identifier,
        role=user_role,
        keywords=keywords,
        shard=f"shard{shard_index+1}",
        query_time=query_time
    )

    log_query_csv(
        user=user_identifier,
        role=user_role,
        keywords=keywords,
        shard=f"shard{shard_index+1}",
        query_time=query_time
    )


    tracker.record_access(keywords)

    print(f"\nQuery Time: {query_time} seconds")

    result_string = str(results)
    result_hash = hashlib.sha256(result_string.encode()).hexdigest()

    block = blockchain.add_block(query_hash, result_hash)

    print("\n🔗 Blockchain Entry:")
    print("Block Hash:", block.hash)
    print("Previous Hash:", block.prev_hash)

    is_valid = blockchain.verify_chain()

    print("\n🔍 Blockchain Status:", "✅ VALID" if is_valid else "❌ TAMPERED")

    # --------------------------
    # Step 5: Output Results
    # --------------------------
    print("\n===== RESULTS =====\n")

    if not results:
        print("❌ No results found")
        return

    for i, r in enumerate(results, 1):
        print(f"Result {i}:")
        print("ID:", r.get("id"))

        if "plaintext" in r:
            print("Decrypted:", r["plaintext"])
        else:
            print("Ciphertext only (no permission)")

        print("-" * 40)


    '''
    for keywords in queries:                # Testing access pattern leakage with repeated queries
        print("\nRunning Query:", keywords)
        
        trapdoors = se.generate_and_trapdoor(keywords)

        start = time.time()

        results, shard_index = engine.secure_read(
            trapdoors=trapdoors,
            user_role=user_role,
            user_identifier=user_identifier
        )

        end = time.time()

        query_time = round(end - start, 6)

        log_query(...)
        log_query_csv(...)

        tracker.record_access(keywords)
    '''

    tracker.print_patterns()


# ==============================
# ENTRY POINT
# ==============================

if __name__ == "__main__":
    # Choose mode

    # 🔹 Demo Mode
    #run_pipeline()

    # 🔹 Benchmark Mode (uncomment when needed)
    #run_benchmark()

    #run_keyword_benchmark()

    run_shard_benchmark()

    