import psycopg2
from app.crypto.encrypt import encrypt_data

conn = psycopg2.connect(
    dbname="shard3",
    user="postgres",
    password="2002",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

def insert_user(username, email, password):
    """
    Inserts encrypted user data into shard2.
    Shard selection logic will be handled by the coordinator layer.
    """
    email_nonce, email_cipher = encrypt_data(email)
    pass_nonce, pass_cipher = encrypt_data(password)

    query = """
    INSERT INTO secure_users
    (username, email_cipher, email_nonce, password_cipher, password_nonce)
    VALUES (%s, %s, %s, %s, %s)
    """

    cur.execute(query, (
        username,
        email_cipher,
        email_nonce,
        pass_cipher,
        pass_nonce
    ))
    conn.commit()
