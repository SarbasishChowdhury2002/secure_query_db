# 🔐 Secure Query Processing over Encrypted and Sharded Databases

## 📌 Overview

This project implements a **secure, scalable query system** that enables searching over **encrypted data** stored across **sharded databases**, while preserving confidentiality and access control.

It integrates:
- 🔒 Encryption (AES-256-GCM)
- 🔍 Searchable Encryption (HMAC-based)
- 🧠 Secure Query Processing
- 📦 Sharding
- 🛡️ Role-Based Access Control (RBAC)
- 🔗 Blockchain-based Audit Logging
- 🎨 Streamlit UI for real-time interaction


## 🎯 Problem Statement
Traditional databases cannot efficiently query encrypted data without exposing sensitive information.

This project solves:
- Secure search over encrypted data
- Privacy-preserving query execution
- Scalable querying using sharding
- Controlled access using RBAC


## ⚙️ System Architecture

User → Trapdoor Generation → Query Coordinator → Shard Routing → Encrypted Search → Decryption → Blockchain Logging


## 🚀 Key Features

### 🔐 Encryption
- AES-256-GCM encryption
- Data encrypted at application layer
- Keys never stored in database

### 🔍 Searchable Encryption
- Keywords converted into HMAC tokens
- Enables search without revealing plaintext

### 🔑 Trapdoor Queries
- Query keywords converted into secure trapdoors
- Matching done on encrypted tokens

### 🔎 Multi-keyword AND Search
- Supports multiple keyword queries
- Improves precision and efficiency

### 📦 Sharding
- Deterministic routing using SHA-256 hashing
- Improves scalability and reduces load

### 🛡️ RBAC (Access Control)
- Admin / Analyst / User roles
- Separate permissions for search and decryption

### 🔄 Key Management
- Versioned encryption keys
- Supports secure key rotation

### 🔗 Blockchain Logging
- Query and result hashes stored in hash chain
- Ensures tamper-proof audit logs

### 🎨 UI (Streamlit)
- Interactive query interface
- Displays:
  - Trapdoors
  - Selected shard
  - Query time
  - Results
  - Blockchain logs



## 📊 Experimental Evaluation

Experiments conducted on:
- Dataset sizes: 1K, 5K, 10K
- Keyword variations (1, 2, 3 keywords)
- Shard configurations (1, 2, 3 shards)

### Observations:
- Query time increases with dataset size
- Multi-keyword queries reduce result size → faster queries
- Sharding improves scalability (limited by system constraints)



## 🧪 Tech Stack

- Python
- Streamlit
- PostgreSQL
- Cryptography (AES-GCM)
- Passlib (bcrypt)
- Hashlib / HMAC



## 📁 Project Structure

secure_query_db/
│
├── app/
│ ├── auth/
│ ├── blockchain/
│ ├── coordinator/
│ ├── crypto/
│ ├── db/
│ ├── experiments/
│ ├── ui/
│
├── report/
├── requirements.txt
└── README.md



## ▶️ How to Run

1. Clone repository
git clone <repo-link>
cd secure_query_db
2. Install dependencies
pip install -r requirements.txt
3. Run the application
streamlit run app/ui/app.py

### 🖥️ Demo Flow
Enter User ID and Role
Input keywords (comma-separated)
Run query

### System performs:
Trapdoor generation
Shard routing
Encrypted search
Decryption (if authorized)
Blockchain logging

### 🔐 Security Analysis
Data remains encrypted at rest
Keywords never exposed
RBAC enforces controlled access
Blockchain ensures log integrity

### ⚠️ Limitation:
Access pattern leakage possible (common in searchable encryption systems)

### 🚀 Future Work
OR-based queries
Ranked search
Full distributed deployment
Advanced leakage prevention techniques

### 👨‍💻 Authors
Sarbasish Chowdhury
Kunal Lagad
