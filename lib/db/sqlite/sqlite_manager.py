import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lib.db.entity.host import Host, HostBase
from lib.db.sqlite.dao.dao_host import select_host_info

logging.basicConfig(level=logging.DEBUG)

# create default data
def add_default_data(session):
    default_hosts = [
        Host(HOST_NAME="host01", IP="192.168.56.50"),
        Host(HOST_NAME="host02", IP="192.168.56.51")
    ]
    session.add_all(default_hosts)
    session.commit()


class SqliteManager:

    def __init__(self):
        self.connect_info = None
        self.session = None

    def get_db_session(self, connect_info):
        self.connect_info = connect_info

        if not os.path.exists(connect_info.db_file):
            engine = create_engine(connect_info.get_connect_string())
            HostBase.metadata.create_all(engine)
            is_created = True
        else:
            engine = create_engine(connect_info.get_connect_string())
            is_created = False

        Session = sessionmaker(bind=engine)
        session = Session()

        if is_created:
            add_default_data(session)

        return session

    def select_host_info(self, name):
        if self.session is None:
            self.session = self.get_db_session()

        return select_host_info(self.session, name)
