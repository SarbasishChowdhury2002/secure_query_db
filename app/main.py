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

from app.coordinator.query_router import ShardRouter

router = ShardRouter()

users = ["sarbasish", "kunal", "rohit"]

for u in users:
    shard = router.route(u)
    print(f"{u} → {shard.__name__}")