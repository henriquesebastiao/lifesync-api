from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from lifesync.core.database import get_session
from lifesync.core.security import get_current_user
from lifesync.models import Account, User
from lifesync.schemas.finance.account import AccountBase, AccountList, AccountSchema
from lifesync.utils.message import AlreadyExists

router = APIRouter(prefix='/finance/accounts', tags=['Finance'])


@router.post(
    '',
    response_model=AccountSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_account(
    schema: AccountBase,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    db_account = session.scalar(
        select(Account).where(
            (Account.account_holder_id == current_user.id) & (Account.name == schema.name)
        )
    )

    if db_account:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=AlreadyExists.ACCOUNT)

    db_account = Account(**schema.model_dump(), account_holder_id=current_user.id)

    session.add(db_account)
    session.commit()
    session.refresh(db_account)

    return db_account


@router.get('/all', response_model=AccountList)
def get_all_account(
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    db_accounts = session.scalars(
        select(Account).where(Account.account_holder_id == current_user.id)
    )

    return {'accounts': db_accounts.all()}
