from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, Date, select

Base = declarative_base()

class Member(Base):
    __tablename__ = 'E_MEMBER'
    MEMBER_UID = Column(Integer, primary_key=True)
    OEM_UID = Column(Integer, nullable=True)
    PLANCHANGE_UID = Column(Integer, nullable=True)
    INVOICE_UID = Column(Integer, nullable=True)
    USERNAME = Column(String, nullable=True)
    CREDIT = Column(DECIMAL, nullable=False)
    NONPAYFEE = Column(DECIMAL, nullable=False)
    XARBID = Column(Integer, nullable=True)
    PAYPALPROFILE_UID = Column(String, nullable=True)
    NEXTBILLINGDATE = Column(Date, nullable=True)
    NEGATIVE_CREDIT_THRESHOLD = Column(DECIMAL, nullable=False)
    TIMEZONE = Column(String, nullable=True)
    DELETEFLAG = Column(Integer, nullable=True)
