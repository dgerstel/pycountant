from pydantic import BaseModel, HttpUrl

from typing import Sequence


class Transfer(BaseModel):
    id: int
    amount: int
    client: str
    vat: int
    descr: str


class TransfersSearchResults(BaseModel):
    results: Sequence[Transfer]


class TransferCreate(BaseModel):
    amount: int
    client: str
    vat: int
    descr: str
    submitter_id: int
