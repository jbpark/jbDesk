from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Emp(Base):
    __tablename__ = 'EMP'
    NO = Column("EMPNO", Integer, primary_key=True)
    NAME = Column("ENAME", String, nullable=True)
    JOB = Column("JOB", String, nullable=True)
