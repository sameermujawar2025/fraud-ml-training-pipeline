import logging
from datetime import timedelta
from tao_app.utils.time_utils import utc_now
from tao_app.models.user_behavior_record import UserBehaviorRecord

logger=logging.getLogger(__name__)

class PipelineService:
    def __init__(self, csv_loader, transaction_repository, user_behavior_repository, blacklist_repository, settings):
        self.loader=csv_loader
        self.txn_repo=transaction_repository
        self.beh_repo=user_behavior_repository
        self.bl_repo=blacklist_repository
        self.settings=settings

    def run_pipeline(self):
        logger.info("Running pipeline")

        txns = self.loader.load_transactions(self.settings.csv_transactions_path)
        if not txns:
            logger.warning("No transactions loaded from CSV.")
            return

        # Use REAL system time, not CSV's max timestamp
        now = max(t.timestamp for t in txns)
        cutoff = now - timedelta(hours=1)

        # Filter last 1-hour records
        last_hour = [t for t in txns if t.timestamp >= cutoff]

        logger.info(f"Loaded {len(txns)} transactions total.")
        logger.info(f"Filtered {len(last_hour)} transactions for last 1 hour window.")

        # Save last hour dataset
        self.txn_repo.ensure_indexes(self.settings.last_hour_ttl_seconds)
        self.txn_repo.replace_last_hour_transactions(last_hour)

        # Build 60-day user behavior
        win = now - timedelta(days=self.settings.behavior_window_days)
        filt = [t for t in txns if t.timestamp >= win]

        grouped = {}
        for t in filt:
            grouped.setdefault((t.user_id, t.card_number), []).append(t)

        records = []
        for (u, c), g in grouped.items():
            gsorted = sorted(g, key=lambda x: x.timestamp)
            last = gsorted[-1]
            am = [x.amount for x in gsorted]

            rec = UserBehaviorRecord(
                user_id=u,
                card_number=c,
                last_transaction_timestamp=last.timestamp,
                last_amount=last.amount,
                last_country=last.current_country,
                last_latitude=last.current_latitude,
                last_longitude=last.current_longitude,
                total_txn_60d=len(gsorted),
                total_decline_60d=len([x for x in gsorted if x.txn_status == 'DECLINED']),
                avg_amount_60d=sum(am) / len(am),
                max_amount_60d=max(am),
                min_amount_60d=min(am)
            )
            records.append(rec)

        self.beh_repo.ensure_indexes()
        self.beh_repo.replace_behavior(records)

        logger.info(f"User behavior profiles generated: {len(records)}")
        logger.info("Pipeline done")
