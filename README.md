# 🔐 Secure Query Processing over Encrypted and Sharded Databases

> CS850 – Database Security | NITK Surathkal  
> Sarbasish Chowdhury (252IS033)

---

## 📌 Overview

A secure, scalable query system that enables keyword search over **AES-256-GCM encrypted data** stored across **sharded databases**, without exposing plaintext to the database layer.

**End-to-end pipeline:**
User Query → Trapdoor Generation → Shard Routing → Encrypted Search → Decryption → Audit Log

---

## 🚀 Key Features

| Feature | Implementation |
|---|---|
| Encryption | AES-256-GCM, application-layer, unique nonce per record |
| Searchable Encryption | HMAC-SHA256 tokens — keywords never exposed to DB |
| Trapdoor Queries | Client generates trapdoor; shard matches on encrypted tokens |
| Multi-keyword AND Search | All tokens must match — improves precision and speed |
| Shard Routing | Deterministic SHA-256 hashing: `Shard(U) = SHA256(U) mod N` |
| RBAC | Admin / Analyst / Auditor — separate search and decrypt permissions |
| Key Management | Versioned AES keys, supports rotation without re-encryption |
| Audit Logging | Tamper-evident hash chain (SHA-256 linked blocks) |
| REST API | FastAPI with auto-generated interactive docs at `/docs` |
| UI | Streamlit interactive interface |

---

## ⚙️ Setup

### 1. Clone and install
```bash
git clone <repo-url>
cd secure_query_db
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 2. Create `.env` in project root
```env
SEARCH_KEY=your-secret-key-here
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432
```

---

## ▶️ How to Run

### Streamlit UI
```bash
streamlit run app/ui/application.py
```
Opens at `http://localhost:8501`

### REST API
```bash
uvicorn app.api.routes:app --reload
```
- API: `http://127.0.0.1:8000`
- Interactive docs: `http://127.0.0.1:8000/docs`

### API Usage Example
```bash
curl -X POST http://127.0.0.1:8000/query \
  -H "Content-Type: application/json" \
  -d '{"user_identifier": "sarbasish", "user_role": "admin", "keywords": ["salary", "bonus"]}'
```

### Run Tests
```bash
pytest tests/test_pipeline.py -v --cov=app --cov-report=term-missing
```

### Run Demo Pipeline
```bash
python -m app.main
```

### Run Benchmarks
```bash
python -m app.main --benchmark           # Dataset size vs query time
python -m app.main --keyword-benchmark   # Keyword count vs query time
python -m app.main --shard-benchmark     # Shard count vs query time
```

---

## 🧪 Test Results
tests/test_pipeline.py::test_encrypt_decrypt_roundtrip          PASSED

tests/test_pipeline.py::test_trapdoor_matches_token             PASSED

tests/test_pipeline.py::test_different_keywords_different_tokens PASSED

tests/test_pipeline.py::test_multi_keyword_trapdoor_count       PASSED

tests/test_pipeline.py::test_admin_can_search_and_decrypt       PASSED

tests/test_pipeline.py::test_analyst_cannot_decrypt             PASSED

tests/test_pipeline.py::test_unknown_role_rejected              PASSED

tests/test_pipeline.py::test_shard_routing_is_deterministic     PASSED

tests/test_pipeline.py::test_different_users_can_route_differently PASSED
9 passed | Coverage: rbac.py 100%, crypto/search.py 100%, query_router.py 100%

---

## 📊 Experimental Results

### Dataset Size vs Query Time
| Dataset Size | Query Time (sec) |
|---|---|
| 1,000 | 0.001001 |
| 5,000 | 0.002972 |
| 10,000 | 0.010998 |

### Keywords vs Query Time
| Keywords | Query Time (sec) |
|---|---|
| 1 | 0.023597 |
| 2 | 0.008600 |
| 3 | 0.007202 |

> More keywords = faster queries due to AND-filtering reducing result set size.

### Shards vs Query Time
| Shards | Query Time (sec) |
|---|---|
| 1 | 0.007004 |
| 2 | 0.006251 |
| 3 | 0.006331 |

> 3-shard overhead explained by Python GIL limiting ThreadPoolExecutor on in-memory data.

---

## 🔐 Security Analysis

| Attack | Traditional DB | This System |
|---|---|---|
| DB breach | All plaintext exposed | Only ciphertext visible |
| Keyword inference | Query logs reveal keywords | Only HMAC tokens visible |
| Privilege escalation | No enforcement | RBAC blocks decryption |
| Log tampering | Undetected | Hash chain breaks — detected |
| Password theft | Plaintext or weak hash | bcrypt — unrecoverable |

**Known limitation:** Access pattern leakage — query frequency and co-occurrence can be inferred without learning keywords. Academic solution: OXT protocol (Cash et al., 2013).

---

## 📁 Project Structure
secure_query_db/

├── app/

│   ├── api/routes.py              # FastAPI REST endpoints

│   ├── auth/rbac.py               # Role-based access control

│   ├── blockchain/ledger.py       # Tamper-evident audit log

│   ├── config.py                  # pydantic-settings configuration

│   ├── coordinator/               # Shard routing

│   ├── crypto/                    # AES-256-GCM + HMAC searchable encryption

│   ├── db/                        # Shard storage + secure query engine

│   ├── experiments/               # Benchmarks + dataset generation

│   ├── security/key_manager.py    # Versioned key management

│   ├── services/query_service.py  # Service layer (pipeline orchestration)

│   ├── ui/application.py          # Streamlit UI

│   └── utils/                     # Logger, access pattern tracker

├── tests/test_pipeline.py         # pytest test suite (9 tests)

├── conftest.py                    # pytest configuration

├── report/project_report.docx     # Full technical report

├── requirements.txt

├── .env                           # Secrets — never committed

└── README.md

---

## 🧰 Tech Stack

Python · FastAPI · Streamlit · PostgreSQL · AES-256-GCM · HMAC-SHA256 · bcrypt · pydantic-settings · pytest