from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base

OrderBase = declarative_base()


class Order(OrderBase):
    __tablename__ = 'orders'
    ORDER_UID = Column("id", Integer, primary_key=True)
    CUSTOMER_NAME = Column("customer_name", String, nullable=True)
    PRODUCT = Column("product", String, nullable=True)
    QUANTITY = Column("quantity", Integer, nullable=True)
    ORDER_DATE = Column("order_date", Date, nullable=True)
