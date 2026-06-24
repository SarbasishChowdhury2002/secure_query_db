import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
from app.blockchain.ledger import BlockchainLogger
from app.services.query_service import QueryService
from app.experiments.dataset_generator import generate_dataset
from app.db import shard1, shard2, shard3


# ==============================
# Initialize
# ==============================
if "blockchain" not in st.session_state:
    st.session_state.blockchain = BlockchainLogger()

if "query_service" not in st.session_state:
    st.session_state.query_service = QueryService(st.session_state.blockchain)

if "data_loaded" not in st.session_state:
    dataset = generate_dataset(1000)
    shard1.load_dataset(dataset[0::3])
    shard2.load_dataset(dataset[1::3])
    shard3.load_dataset(dataset[2::3])
    st.session_state.data_loaded = True

blockchain = st.session_state.blockchain
service = st.session_state.query_service


# ==============================
# UI
# ==============================
st.title("🔐 Secure Query System")
st.markdown("---")
st.info("Flow: Query → Trapdoor → Shard Routing → Encrypted Search → Decryption → Blockchain Logging")
st.caption("🔐 All data is encrypted using AES-256. Search is performed on secure tokens.")
st.markdown("---")

user_identifier = st.text_input("User ID", "sarbasish")
user_role = st.selectbox("Role", ["admin", "analyst", "user"])
keywords_input = st.text_input("Enter keywords (comma separated)", "salary,bonus")

if st.button("Run Secure Query"):
    try:
        keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]

        result = service.run_query(
            user_identifier=user_identifier,
            user_role=user_role,
            keywords=keywords
        )

        st.write("🔍 Processed Keywords:", keywords)

        # Query Info
        st.subheader("📊 Query Info")
        st.write(f"⏱ Time: {result['query_time'] * 1000:.6f} ms")
        st.success(f"📦 Routed to Shard: {result['shard_name']}")
        st.write("👤 Role:", user_role)

        # Trapdoors
        st.subheader("🔑 Trapdoor Generation")
        for keyword, trapdoor in result["trapdoors"].items():
            st.write(f"Keyword: {keyword}")
            st.code(trapdoor)

        # Results
        st.markdown("---")
        st.subheader(f"📄 Results ({result['result_count']} records)")

        if not result["results"]:
            st.info("No matching records found for given keywords")
        else:
            for r in result["results"]:
                if "plaintext" in r:
                    st.code(r["plaintext"])
                else:
                    st.warning("Encrypted result (no permission)")

        # Blockchain
        st.markdown("---")
        st.subheader("🔗 Blockchain Log")
        st.write("Block Hash:")
        st.code(result["block_hash"])
        st.write("Previous Hash:")
        st.code(result["prev_hash"])

        st.markdown("---")
        st.write("🔐 All sensitive data remains encrypted. Only authorized users can decrypt results.")

    except ValueError as e:
        st.error(f"⚠️ Invalid input: {str(e)}")

    except PermissionError:
        st.error("🚫 You are not authorized to perform this action")

    except Exception as e:
        st.error(f"Something went wrong: {str(e)}")