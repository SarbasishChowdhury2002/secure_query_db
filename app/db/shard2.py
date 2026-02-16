import psycopg2
from app.crypto.encrypt import encrypt_data

conn = psycopg2.connect(
    dbname="shard2",
    user="postgres",
    password="2002",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

def insert_user(username, email, password):
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
nonce, ciphertext, key_version = encrypt_data("Employee Salary: 200000")

SHARD_DATA = [
    {
        "id": "s2-1",
        "tokens": ["token_salary", "token_bonus"],
        "nonce": nonce,
        "ciphertext": ciphertext,
        "key_version": key_version
    }
]


def read_all():
    return SHARD_DATA

