import psycopg2
from app.crypto.encrypt import encrypt_data

from app.crypto.search import SearchableEncryption

#from app.utils.constants import SEARCH_KEY

import os
from dotenv import load_dotenv
load_dotenv()

search_key = os.getenv("SEARCH_KEY")

se = SearchableEncryption(search_key)

conn = psycopg2.connect(
    dbname="shard3",
    user="postgres",
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

cur = conn.cursor()

def insert_user(username, email, password):
    """
    Inserts encrypted user data into shard3.
    Shard selection logic will be handled by the coordinator layer.
    """
    email_nonce, email_cipher, email_key_version = encrypt_data(email)
    pass_nonce, pass_cipher, pass_key_version = encrypt_data(password)

    query = """
    INSERT INTO secure_users
    (username,
     email_cipher, email_nonce, email_key_version,
     password_cipher, password_nonce, password_key_version)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    cur.execute(query, (
        username,
        email_cipher,
        email_nonce,
        email_key_version,
        pass_cipher,
        pass_nonce,
        pass_key_version
    ))
    conn.commit()



# Simulate real encryption
nonce, ciphertext, key_version = encrypt_data("Employee Salary: 300000")

'''SHARD_DATA = [
    {
        "id": "s3-1",
        "tokens": ["token_salary", "token_bonus"],
        "nonce": nonce,
        "ciphertext": ciphertext,
        "key_version": key_version
    }
]'''

# In-memory shard storage for experiments
SHARD_DATA = []


def read_all():
    return SHARD_DATA


def load_dataset(dataset):
    global SHARD_DATA

    SHARD_DATA = []

    for record in dataset:
        nonce, ciphertext, key_version = encrypt_data(record["text"])

        tokens = [se.generate_token(k) for k in record["keywords"]]

        SHARD_DATA.append({
            "id": record["id"],
            "tokens": tokens,
            "nonce": nonce,
            "ciphertext": ciphertext,
            "key_version": key_version
        })