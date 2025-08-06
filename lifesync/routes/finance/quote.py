from datetime import datetime, timedelta
from typing import Annotated
from zoneinfo import ZoneInfo

import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from lifesync.core.database import get_session
from lifesync.core.security import get_current_user
from lifesync.models import Quote, User
from lifesync.schemas.finance.quotes import QuoteCreate, QuoteSchema, QuoteUpdate
from lifesync.utils.database import upattr
from lifesync.utils.message import AlreadyExists, DoesNotExist

router = APIRouter(prefix='/finance/quotes', tags=['Finance'])


@router.post(
    '',
    response_model=QuoteSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_currency_quote(
    schema: QuoteCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    db_quote = session.scalar(select(Quote).where(Quote.code == schema.code))

    if db_quote:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=AlreadyExists.QUOTE)

    quote_response = httpx.get(f'https://economia.awesomeapi.com.br/last/{schema.code.upper()}')

    if quote_response.status_code == status.HTTP_200_OK:
        quote_response = quote_response.json()[f'{schema.code}'.replace('-', '')]

        db_quote = Quote(
            code=schema.code,
            high=float(quote_response['high']),
            low=float(quote_response['low']),
            varBid=float(quote_response['varBid']),
            pctChange=float(quote_response['pctChange']),
            bid=float(quote_response['bid']),
            ask=float(quote_response['ask']),
        )

        session.add(db_quote)
        session.commit()
        session.refresh(db_quote)

        return db_quote
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='An error occurred while registering the quote',
        )


@router.get('/{code}', response_model=QuoteSchema)
def get_currency_quote(
    code: str,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session),
):
    code = code.upper()
    db_quote = session.scalar(select(Quote).where(Quote.code == code))

    if not db_quote:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=DoesNotExist.QUOTE)

    one_hour_ago = datetime.now(tz=ZoneInfo('UTC')) - timedelta(hours=1)

    # Se o horário da última atualização for mais recente ou igual a uma hora atrás,
    # então o dado ainda está válido e não precisa ser atualizado.
    if db_quote.updated_at.timestamp() >= one_hour_ago.timestamp():
        return db_quote

    quote_response = httpx.get(f'https://economia.awesomeapi.com.br/last/{code}')

    if quote_response.status_code == status.HTTP_200_OK:
        quote_response = quote_response.json()[f'{code}'.replace('-', '')]

        update_schema = QuoteUpdate(
            high=float(quote_response['high']),
            low=float(quote_response['low']),
            varBid=float(quote_response['varBid']),
            pctChange=float(quote_response['pctChange']),
            bid=float(quote_response['bid']),
            ask=float(quote_response['ask']),
        )

        upattr(update_schema, db_quote)

        session.add(db_quote)
        session.commit()
        session.refresh(db_quote)

        return db_quote
