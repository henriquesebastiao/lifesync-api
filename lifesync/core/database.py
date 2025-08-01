from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from lifesync.core.settings import get_settings

engine = create_engine(get_settings().DATABASE_URL)


def get_session():
    with Session(engine, expire_on_commit=False) as session:
        yield session
