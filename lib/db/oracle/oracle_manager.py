import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lib.db.oracle.dao.dao_member import select_member_info
from lib.db.oracle.dao.dao_test_member import select_test_member_info

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

    def select_member_info(self, member_uid, dataset_name):
        if self.session is None:
            self.session = self.get_db_session()

        return select_member_info(self.session, member_uid, dataset_name)

    def select_test_member_info(self, name):
        if self.session is None:
            self.session = self.get_db_session()

        return select_test_member_info(self.session, name)
