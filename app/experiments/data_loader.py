from app.experiments.dataset_generator import generate_dataset
from app.coordinator.shard_insert_router import ShardInsertRouter
from app.crypto.search import SearchableEncryption
from app.utils.constants import SEARCH_KEY

# initialize
router = ShardInsertRouter()
se = SearchableEncryption(SEARCH_KEY)


def load_data(size):
    dataset = generate_dataset(size)

    for record in dataset:
        user_id = record["id"]

        # Insert user (encrypted email + password dummy)
        router.insert_user(
            user_identifier=user_id,
            username=user_id,
            email=f"{user_id}@example.com",
            password="pass123"
        )

        # NOTE: For now we are not storing keywords in DB
        # (still using in-memory shard tokens)
    
    print(f"Loaded {size} records successfully")