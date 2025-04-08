from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base

HostBase = declarative_base()


class Host(HostBase):
    __tablename__ = 'hosts'
    HOST_UID = Column("id", Integer, primary_key=True)
    HOST_NAME = Column("host_name", String, nullable=True)
    IP = Column("ip", String, nullable=True)
