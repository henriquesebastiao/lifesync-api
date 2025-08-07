from pydantic import BaseModel


class AccountBase(BaseModel):
    name: str
    balance: int
    color: str


class AccountSchema(AccountBase):
    id: int
    account_holder_id: int


class AccountList(BaseModel):
    accounts: list[AccountSchema]
