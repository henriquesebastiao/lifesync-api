from datetime import datetime

from pydantic import BaseModel


class QuoteCreate(BaseModel):
    code: str


class QuoteBase(BaseModel):
    code: str
    high: float
    low: float
    varBid: float
    pctChange: float
    bid: float
    ask: float


class QuoteUpdate(BaseModel):
    high: float | None = None
    low: float | None = None
    varBid: float | None = None
    pctChange: float | None = None
    bid: float | None = None
    ask: float | None = None


class QuoteSchema(QuoteBase):
    id: int
    updated_at: datetime
