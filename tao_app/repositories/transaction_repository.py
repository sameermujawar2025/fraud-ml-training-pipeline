# repositories/transaction_repository.py
from pymongo import ASCENDING
import logging

logger = logging.getLogger(__name__)

class TransactionRepository:
    COLLECTION_NAME = "transactions_90_days"

    def __init__(self, client, db_name):
        self.col = client[db_name][self.COLLECTION_NAME]

    def ensure_indexes(self, ttl_seconds):
        # AUTO-DELETE after 90 days
        self.col.create_index(
            [("timestamp", ASCENDING)],
            expireAfterSeconds=ttl_seconds
        )

        self.col.create_index([("transaction_id", ASCENDING)], unique=True)

    def replace_90day_transactions(self, txns):
        self.col.delete_many({})
        if txns:
            self.col.insert_many([t.model_dump() for t in txns])
