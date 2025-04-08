import logging

from sqlalchemy.orm import aliased

from lib.db.entity.host import Host


def select_host_info(session, name):
    print("select_host_info")
    host = aliased(Host)

    host_resp = session.query(host) \
        .filter(host.HOST_NAME == name).first()

    if host_resp is None:
        logging.debug("cannot found host")
        return

    return host_resp
