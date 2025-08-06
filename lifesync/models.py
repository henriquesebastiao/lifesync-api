from datetime import datetime
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

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


@table_registry.mapped_as_dataclass
class Quotes:
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
