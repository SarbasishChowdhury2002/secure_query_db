from fastapi import FastAPI

app = FastAPI(title="Secure Query Processing over Encrypted & Sharded DBs")

@app.get("/")
def root():
    return {"status": "System running on Windows"}