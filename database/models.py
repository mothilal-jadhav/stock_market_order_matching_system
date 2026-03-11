from sqlalchemy import Column, Integer, Float, String
from database.db import Base


class Trade(Base):

    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)

    buy_order_id = Column(String)

    sell_order_id = Column(String)

    price = Column(Float)

    quantity = Column(Integer)