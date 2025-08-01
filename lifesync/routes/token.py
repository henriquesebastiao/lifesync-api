from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from lifesync.core.database import get_session
from lifesync.core.security import (
    create_access_token,
    get_current_user,
    verify_password,
)
from lifesync.models import User
from lifesync.schemas.token import Token

router = APIRouter(tags=['Token'])


@router.post('/token', response_model=Token)
def login_for_access_token(
    session: Annotated[Session, Depends(get_session)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    invalid_credentials_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='Incorrect email or password',
    )

    user = session.scalar(select(User).where(User.email == form_data.username))

    if not user:
        raise invalid_credentials_exception
    elif not verify_password(form_data.password, user.password):
        raise invalid_credentials_exception

    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'Bearer'}


@router.post('/refresh_token', response_model=Token)
def refresh_access_token(user: User = Depends(get_current_user)):
    new_access_token = create_access_token(data={'sub': user.email})

    return {'access_token': new_access_token, 'token_type': 'bearer'}
