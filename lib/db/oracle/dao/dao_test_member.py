import logging

from sqlalchemy.orm import aliased

from lib.db.entity.member import Member
from lib.db.entity.test_member import TestMember


def select_test_member_info(session, name):
    print("select_test_member_info")
    member = aliased(TestMember)

    member_resp = session.query(member) \
        .filter(member.name == name).first()

    if member_resp is None:
        logging.debug("cannot found memeber")
        return

    return member_resp
