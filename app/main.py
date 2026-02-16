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

