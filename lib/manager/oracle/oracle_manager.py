import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logging.basicConfig(level=logging.DEBUG)


class OracleManager:

    def __init__(self):
        self.connect_info = None
        self.session = None

    def get_db_session(self, connect_info):
        self.connect_info = connect_info

        engine = create_engine(connect_info.get_connect_string())
        Session = sessionmaker(bind=engine)
        return Session()
