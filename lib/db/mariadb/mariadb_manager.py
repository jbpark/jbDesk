import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lib.db.mariadb.dao.dao_order import select_order_info

logging.basicConfig(level=logging.DEBUG)


class MariadbManager:

    def __init__(self):
        self.connect_info = None
        self.session = None

    def get_db_session(self, connect_info):
        self.connect_info = connect_info

        engine = create_engine(connect_info.get_connect_string())
        Session = sessionmaker(bind=engine)
        return Session()

    def select_order_info(self, name):
        if self.session is None:
            self.session = self.get_db_session()

        return select_order_info(self.session, name)
