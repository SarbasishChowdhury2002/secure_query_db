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
