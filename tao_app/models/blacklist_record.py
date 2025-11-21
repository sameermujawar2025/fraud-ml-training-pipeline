# models/blacklist_record.py
from pydantic import BaseModel
from typing import Optional

class BlacklistRecord(BaseModel):
    user_id: Optional[str] = None
    card_number: Optional[str] = None
    ip_address: Optional[str] = None

    reason: str
    source: str
