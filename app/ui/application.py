import streamlit as st
import time
import hashlib
from app.blockchain.ledger import BlockchainLogger
from app.crypto.search import SearchableEncryption
from app.db.secure_query import SecureQueryEngine
from app.utils.constants import SEARCH_KEY
from app.experiments.dataset_generator import generate_dataset
from app.db import shard1, shard2, shard3


# Initialize
se = SearchableEncryption(SEARCH_KEY)
engine = SecureQueryEngine()

if "blockchain" not in st.session_state:
    st.session_state.blockchain = BlockchainLogger()

blockchain = st.session_state.blockchain


st.title("🔐 Secure Query System")
st.markdown("---")

st.info(
    "Flow: Query → Trapdoor → Shard Routing → Encrypted Search → Decryption → Blockchain Logging"
)

st.caption("🔐 All data is encrypted using AES-256. Search is performed on secure tokens.")
st.markdown("---")


# Load dataset once
if "data_loaded" not in st.session_state:
    dataset = generate_dataset(1000)

    # split dataset across shards
    shard1.load_dataset(dataset[0::3])
    shard2.load_dataset(dataset[1::3])
    shard3.load_dataset(dataset[2::3])
    st.session_state.data_loaded = True


# --------------------------
# User Inputs
# --------------------------
user_identifier = st.text_input("User ID", "sarbasish")
user_role = st.selectbox("Role", ["admin", "analyst", "user"])

keywords_input = st.text_input("Enter keywords (comma separated)", "salary,bonus")

# --------------------------
# Run Query
# --------------------------
if st.button("Run Secure Query"):

    try:
        keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]

        if not keywords:
            st.error("Please enter at least one keyword")
            st.stop()

        st.write("🔍 Processed Keywords:", keywords)

        trapdoors = se.generate_and_trapdoor(keywords)

        with st.spinner("🔐 Running secure query..."):
            start = time.time()

            results, shard_index = engine.secure_read(
                trapdoors=trapdoors,
                user_role=user_role,
                user_identifier=user_identifier
            )

            end = time.time()

        query_time = round(end - start, 6)

        # Blockchain logging
        query_string = f"{user_identifier}:{keywords}"
        query_hash = hashlib.sha256(query_string.encode()).hexdigest()

        result_string = str(results)
        result_hash = hashlib.sha256(result_string.encode()).hexdigest()

        block = blockchain.add_block(query_hash, result_hash)


        # --------------------------
        # Display Info
        # --------------------------
        st.subheader("📊 Query Info")
        st.write(f"⏱ Time: {query_time * 1000:.6f} ms")
        st.success(f"📦 Routed to Shard: shard{shard_index+1}")
        st.write("👤 Role:", user_role)

        # --------------------------
        # Trapdoors
        # --------------------------
        st.subheader("🔑 Trapdoor Generation")

        for k, t in zip(keywords, trapdoors):
            st.write(f"Keyword: {k}")
            st.code(t)

        # --------------------------
        # Results
        # --------------------------
        st.markdown("---")
        st.subheader(f"📄 Results ({len(results)} records)")

        if not results:
            st.info("No matching records found for given keywords")
        else:
            for r in results:
                if "plaintext" in r:
                    st.code(r["plaintext"])
                else:
                    st.warning("Encrypted result (no permission)")

        st.markdown("---")
        st.subheader("🔗 Blockchain Log")

        st.write("Block Hash:")
        st.code(block.hash)

        st.write("Previous Hash:")
        st.code(block.prev_hash)

        st.markdown("---")
        st.write("🔐 All sensitive data remains encrypted. Only authorized users can decrypt results.")

    except PermissionError:
        st.error("🚫 You are not authorized to perform this action")

    except Exception as e:
        st.error(f"Something went wrong: {str(e)}")

