import streamlit as st
import time

from app.crypto.search import SearchableEncryption
from app.db.secure_query import SecureQueryEngine
from app.utils.constants import SEARCH_KEY
from app.experiments.dataset_generator import generate_dataset
from app.db import shard1, shard2, shard3


# Initialize
se = SearchableEncryption(SEARCH_KEY)
engine = SecureQueryEngine()

st.title("🔐 Secure Query System")


# Load dataset once
if "data_loaded" not in st.session_state:
    dataset = generate_dataset(1000)
    shard1.load_dataset(dataset)
    shard2.load_dataset(dataset)
    shard3.load_dataset(dataset)
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

    keywords = [k.strip() for k in keywords_input.split(",")]

    trapdoors = se.generate_and_trapdoor(keywords)

    start = time.time()

    results, shard_index = engine.secure_read(
        trapdoors=trapdoors,
        user_role=user_role,
        user_identifier=user_identifier
    )

    end = time.time()

    query_time = round(end - start, 6)

    # --------------------------
    # Display Info
    # --------------------------
    st.subheader("📊 Query Info")
    st.write("⏱ Time:", query_time, "sec")
    st.write("📦 Shard Used:", f"shard{shard_index+1}")

    # --------------------------
    # Show Trapdoors (BONUS)
    # --------------------------
    st.subheader("🔑 Trapdoors")
    for t in trapdoors:
        st.code(t)

    # --------------------------
    # Results
    # --------------------------
    st.subheader("📄 Results")

    if not results:
        st.error("No results found")
    else:
        for r in results:
            if "plaintext" in r:
                st.success(r["plaintext"])
            else:
                st.warning("Encrypted result (no permission)")


st.write("🔐 Encrypted tokens hidden for security")