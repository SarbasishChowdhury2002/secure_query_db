from app.coordinator.query_router import ShardRouter


class ShardInsertRouter:

    def __init__(self):
        self.router = ShardRouter()

    def insert_user(self, user_identifier, username, email, password):
        shard = self.router.route(user_identifier)

        # Call insert_user function inside correct shard
        shard.insert_user(username, email, password)
        