import logging

from sqlalchemy.orm import aliased

from lib.db.entity.member import Member


def select_member_info(session, member_uid, dataset_name):
    print("select_member_info_by_member_dataset")
    member = aliased(Member)

    member_resp = session.query(member) \
        .filter(member.MEMBER_UID == member_uid).first()

    if member_resp is None:
        logging.debug("cannot found memeber")
        return

    return member_resp
