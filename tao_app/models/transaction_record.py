from datetime import datetime
from pydantic import BaseModel

from datetime import datetime
from pydantic import BaseModel


class TransactionRecord(BaseModel):
    transaction_id: str
    timestamp: datetime

    user_id: str
    card_number: str

    amount: float
    currency: str
    txn_status: str
    transaction_type: str
    payment_channel: str

    device_id: str
    ip_address: str

    current_latitude: float
    current_longitude: float
    current_country: str

    merchant_id: str
    merchant_category_code: str
    merchant_category_desc: str

    customer_risk_category: str
    customer_kyc_status: str
    customer_account_age_days: int

