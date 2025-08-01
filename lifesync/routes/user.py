from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from lifesync.core.database import get_session
from lifesync.core.security import get_current_user, get_password_hash
from lifesync.models import User
from lifesync.schemas import Message
from lifesync.schemas.user import UserCreate, UserSchema, UserUpdate
from lifesync.utils import response
from lifesync.utils.database import upattr
from lifesync.utils.message import AlreadyExists
from lifesync.utils.raises import NotEnoughPermissions

router = APIRouter(prefix='/user', tags=['Usuário'])


@router.post(
    '/',
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
    responses=response.CREATE_USER,
    summary='Cria um novo usuário',
)
def create_user(schema: UserCreate, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.email == schema.email))

    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=AlreadyExists.EMAIL)

    db_user = session.scalar(select(User).where(User.email == schema.email))

    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=AlreadyExists.EMAIL)

    schema.password = get_password_hash(schema.password)

    db_user = User(**schema.model_dump())

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.patch(
    '/{user_id}',
    response_model=UserSchema,
    responses=response.UPDATE_USER,
    summary='Atualiza um usuário',
)
def update_user(
    user_id: int,
    schema: UserUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    if user_id != current_user.id:
        raise NotEnoughPermissions()

    db_user = session.scalar(select(User).where(User.id == user_id))

    if schema.email:
        db_email_exist = session.scalar(select(User).where(User.email == schema.email))

        if db_email_exist:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=AlreadyExists.EMAIL,
            )

    if schema.email:
        db_email_exist = session.scalar(select(User).where(User.email == schema.email))

        if db_email_exist:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=AlreadyExists.EMAIL,
            )

    upattr(schema, db_user)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.delete(
    '/{user_id}',
    response_model=Message,
    responses=response.DELETE_USER,
    summary='Deleta um usuário',
)
def delete_user(
    user_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    if user_id != current_user.id:
        raise NotEnoughPermissions()

    db_user = session.scalar(select(User).where(User.id == user_id))

    session.delete(db_user)
    session.commit()

    return {'message': 'Usuário deletado'}
