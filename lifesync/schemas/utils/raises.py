from pydantic import BaseModel

from lifesync.utils import message


class BaseRaiseModel(BaseModel):
    detail: str


class EmailAlreadyExists(BaseRaiseModel):
    detail: str = message.AlreadyExists.EMAIL


class UserDoesNotExists(BaseRaiseModel):
    detail: str = message.DoesNotExist.USER


class AccountDosNotExists(BaseRaiseModel):
    detail: str = message.DoesNotExist.ACCOUNT
