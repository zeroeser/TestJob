from datetime import datetime as dt

from sqlalchemy import Column, DateTime, Integer

from app.db import Base


class Deliveries(Base):
    """Deliveries database mapping class"""

    number: int = Column(Integer, index=True)
    """порядковый номер в экселе"""

    order_number: int = Column(Integer, index=True, primary_key=True)
    """Номер заказа"""

    price_in_dollar: int = Column(Integer)
    """Цена в долларах"""

    price_in_rub: float = Column(Integer)
    """Цена в рублях"""

    delivery_time: dt = Column(DateTime)
    """Доставка до"""
