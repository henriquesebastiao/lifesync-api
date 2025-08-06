from datetime import datetime
from typing import List, Optional
from zoneinfo import ZoneInfo

from sqlalchemy import ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    """Tabela de usuários do app"""

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[Optional[str]] = mapped_column(default=None)
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now())

    accounts: Mapped[List['Account']] = relationship(
        back_populates='user',
        lazy='immediate',
        init=False,
        default_factory=list,
        cascade='delete',
    )


@table_registry.mapped_as_dataclass
class Quote:
    """Tabela de cotações de moedas consultadas na API AwesomeAPI

    Attributes:
        id (int): Chave primária
        code (str): Código de moeda
        high (float): Máximo
        low (float): Mínimo
        varBid (float): Variação
        pctChange (float): Porcentagem de Variação
        bid (float): Compra
        ask (float): Venda
    """

    __tablename__ = 'quotes'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    code: Mapped[str]
    high: Mapped[float]
    low: Mapped[float]
    varBid: Mapped[float]
    pctChange: Mapped[float]
    bid: Mapped[float]
    ask: Mapped[float]
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=datetime.now(tz=ZoneInfo('UTC'))
    )


@table_registry.mapped_as_dataclass
class Account:
    __tablename__ = 'accounts'
    __table_args__ = (
        # Cada usuário só possa ter uma conta com determinado nome
        UniqueConstraint('account_holder_id', 'name', name='uix_user_account_name'),
    )

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    balance: Mapped[float]
    account_holder_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user: Mapped['User'] = relationship(back_populates='accounts', lazy='immediate', init=False)
