import logging

from sqlalchemy.orm import aliased

from lib.models.db.entity.order import Order


def select_order_info(session, name):
    print("select_order_info")
    order = aliased(Order)

    order_resp = session.query(order) \
        .filter(order.CUSTOMER_NAME == name).first()

    if order_resp is None:
        logging.debug("cannot found order")
        return

    return order_resp
