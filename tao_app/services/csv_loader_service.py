# services/csv_loader_service.py
import pandas as pd
from dateutil.parser import isoparse
import logging

from tao_app.models.blacklist_record import BlacklistRecord
from tao_app.models.transaction_record import TransactionRecord
from tao_app.utils.normalizers import normalize_card_number

logger = logging.getLogger(__name__)

class CsvLoaderService:

    # --------------------------------------------------------
    # Load Transactions CSV
    # --------------------------------------------------------
    def load_transactions(self, path):
        df = pd.read_csv(path)
        out = []

        for _, r in df.iterrows():
            try:
                txn = TransactionRecord(
                    transaction_id=str(r["transaction_id"]),
                    timestamp=isoparse(str(r["timestamp"])),

                    user_id=str(r["user_id"]),
                    card_number=normalize_card_number(r["card_number"]),

                    amount=float(r["amount"]),
                    currency=str(r["currency"]),
                    txn_status=str(r["txn_status"]),
                    transaction_type=str(r["transaction_type"]),
                    payment_channel=str(r["payment_channel"]),

                    device_id=str(r["device_id"]),
                    ip_address=str(r["ip_address"]),

                    current_latitude=float(r["current_latitude"]),
                    current_longitude=float(r["current_longitude"]),
                    current_country=str(r["current_country"]),

                    merchant_id=str(r["merchant_id"]),
                    merchant_category_code=str(r["merchant_category_code"]),
                    merchant_category_desc=str(r["merchant_category_desc"]),

                    customer_risk_category=str(r["customer_risk_category"]),
                    customer_kyc_status=str(r["customer_kyc_status"]),
                    customer_account_age_days=int(r["customer_account_age_days"])
                )
                out.append(txn)

            except Exception as e:
                logger.warning(f"Bad row in Transaction CSV: {e}")

        return out

    # --------------------------------------------------------
    # Load Blacklist CSV (INSIDE THE CLASS!)
    # --------------------------------------------------------
    def load_blacklist(self, path):
        try:
            df = pd.read_csv(path).fillna("")
        except Exception as e:
            logger.error(f"Failed to read Blacklist CSV: {e}")
            raise

        out = []
        for _, row in df.iterrows():
            try:
                record = BlacklistRecord(
                    user_id=row["user_id"] or None,

                    # Normalize card number to safe string
                    card_number=normalize_card_number(row["card_number"]) if row["card_number"] else None,

                    ip_address=row["ip_address"] or None,
                    reason=row["reason"],
                    source=row["source"]
                )
                out.append(record)

            except Exception as e:
                logger.warning(f"Invalid blacklist row skipped: {row.to_dict()}, error={e}")

        return out

