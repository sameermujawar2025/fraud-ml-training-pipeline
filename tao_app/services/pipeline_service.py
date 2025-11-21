# services/pipeline_service.py
import logging
from datetime import timedelta
from tao_app.utils.time_utils import utc_now

logger = logging.getLogger(__name__)

class PipelineService:
    def __init__(
        self,
        csv_loader,
        transaction_repository,
        blacklist_repository,
        settings
    ):
        self.loader = csv_loader
        self.txn_repo = transaction_repository
        self.bl_repo = blacklist_repository
        self.settings = settings

    def run_pipeline(self):
        logger.info("Starting 90-day transaction pipeline...")

        # --------------------------------------------------------
        # 1. LOAD TRANSACTIONS CSV
        # --------------------------------------------------------
        try:
            txns = self.loader.load_transactions(self.settings.csv_transactions_path)
        except Exception as e:
            logger.error(f"Failed to load transactions CSV: {e}")
            return

        if not txns:
            logger.warning("CSV loaded but contains zero valid transactions.")
            return

        # Use system time for cutoff
        now = utc_now()
        cutoff = now - timedelta(days=90)

        # Filter last 90 days
        last_90d = [t for t in txns if t.timestamp >= cutoff]
        dropped = len(txns) - len(last_90d)

        logger.info(f"Total CSV transactions: {len(txns)}")
        logger.info(f"Transactions within last 90 days: {len(last_90d)}")
        logger.info(f"Older transactions discarded: {dropped}")

        if not last_90d:
            logger.warning("No records qualify for last 90 days. Nothing saved.")
            return

        # Save 90-day dataset
        try:
            self.txn_repo.ensure_indexes(self.settings.last_90d_ttl_seconds)
            self.txn_repo.replace_90day_transactions(last_90d)
        except Exception as e:
            logger.error(f"Failed writing 90-day transactions to MongoDB: {e}")
            return

        logger.info("✔ 90-day transaction dataset updated.")

        # --------------------------------------------------------
        # 2. LOAD BLACKLIST CSV (optional)
        # --------------------------------------------------------
        if self.settings.csv_blacklist_path:
            logger.info(f"Loading blacklist CSV: {self.settings.csv_blacklist_path}")

            try:
                blacklist_records = self.loader.load_blacklist(self.settings.csv_blacklist_path)
            except Exception as e:
                logger.error(f"Failed to load blacklist CSV: {e}")
                blacklist_records = []

            if blacklist_records:
                try:
                    self.bl_repo.replace_blacklist(blacklist_records)
                    logger.info(f"✔ Blacklist updated: {len(blacklist_records)} entries")
                except Exception as e:
                    logger.error(f"Failed writing blacklist to MongoDB: {e}")
            else:
                logger.warning("No blacklist records found in CSV.")
        else:
            logger.info("No blacklist CSV path provided. Skipping blacklist load.")

        # --------------------------------------------------------
        # DONE
        # --------------------------------------------------------
        logger.info("✔ Full pipeline execution complete.")
