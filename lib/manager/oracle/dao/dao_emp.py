import logging

from sqlalchemy.orm import aliased

from lib.models.db.entity.emp import Emp


def select_emp_info(session, name):
    print("select_emp_info")
    emp = aliased(Emp)

    resp = session.query(emp) \
        .filter(emp.NAME == name).first()

    if resp is None:
        logging.debug("cannot found emp")
        return

    return resp
