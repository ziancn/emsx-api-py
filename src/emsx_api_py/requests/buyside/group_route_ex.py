"""
Wrapper method to create 'GroupRouteEx' request.
"""

import blpapi
import logging

from typing import List, TypedDict, Unpack, NotRequired

from ..request_service_map import request_service_map


# blpapi names
EMSX_REQUEST_SEQ = blpapi.Name("EMSX_REQUEST_SEQ")
EMSX_SEQUENCE = blpapi.Name("EMSX_SEQUENCE")
EMSX_AMOUNT_PERCENT = blpapi.Name("EMSX_AMOUNT_PERCENT")
EMSX_BROKER = blpapi.Name("EMSX_BROKER")

EMSX_ACCOUNT = blpapi.Name("EMSX_ACCOUNT")
EMSX_BOOKNAME = blpapi.Name("EMSX_BOOKNAME")
EMSX_CFD_FLAG = blpapi.Name("EMSX_CFD_FLAG")
EMSX_CLEARING_ACCOUNT = blpapi.Name("EMSX_CLEARING_ACCOUNT")
EMSX_CLEARING_FIRM = blpapi.Name("EMSX_CLEARING_FIRM")
EMSX_EXEC_INSTRUCTION = blpapi.Name("EMSX_EXEC_INSTRUCTION")
EMSX_GET_WARNINGS = blpapi.Name("EMSX_GET_WARNINGS")
EMSX_GTD_DATE = blpapi.Name("EMSX_GTD_DATE")
EMSX_LIMIT_PRICE = blpapi.Name("EMSX_LIMIT_PRICE")
EMSX_LOCATE_BROKER = blpapi.Name("EMSX_LOCATE_BROKER")
EMSX_LOCATE_ID = blpapi.Name("EMSX_LOCATE_ID")
EMSX_LOCATE_REQ = blpapi.Name("EMSX_LOCATE_REQ")
EMSX_NOTES = blpapi.Name("EMSX_NOTES")
EMSX_ODD_LOT = blpapi.Name("EMSX_ODD_LOT")
EMSX_P_A = blpapi.Name("EMSX_P_A")
EMSX_RELEASE_TIME = blpapi.Name("EMSX_RELEASE_TIME")
EMSX_STOP_PRICE = blpapi.Name("EMSX_STOP_PRICE")
EMSX_TRADER_UUID = blpapi.Name("EMSX_TRADER_UUID")


class GroupRouteExOptional(TypedDict, total=False):
    emsx_account          : NotRequired[str]        # "TestAccount"
    emsx_bookname         : NotRequired[str]        # "TestBook"
    emsx_cfd_flag         : NotRequired[str]        # "0" or "1"
    emsx_clearing_account : NotRequired[str]        # "ClrAccName
    emsx_clearing_firm    : NotRequired[str]        # "FirmName"
    emsx_exec_instruction : NotRequired[str]        # "AnyInst"
    emsx_get_warnings     : NotRequired[str]        # "0" or "1"
    emsx_gtd_date         : NotRequired[str]        # "yyyymmdd"
    emsx_limit_price      : NotRequired[float]      # 123.45
    emsx_locate_broker    : NotRequired[str]        # "CLSA"
    emsx_locate_id        : NotRequired[str]        # "SomeID"
    emsx_locate_req       : NotRequired[str]        # "Y"
    emsx_notes            : NotRequired[str]        # "Some Notes"
    emsx_odd_lot          : NotRequired[str]        # "0" or "1"
    emsx_p_a              : NotRequired[str]        # "p" or "a"
    emsx_release_time     : NotRequired[int]        # 34341
    emsx_request_seq      : NotRequired[str]        # "1001"
    emsx_stop_price       : NotRequired[float]      # 123.5
    emsx_trader_uuid      : NotRequired[int]        # 1234567


def group_route_ex(
        service: blpapi.Service,
        *,
        order_sequences: List[int],
        amount_percentage: float,
        broker: str,
        **kwargs: Unpack[GroupRouteExOptional]
) -> blpapi.Request:
    """

    Args:
        service:
        order_sequences:
        amount_percentage: 100 means routes entire orders, unit is %.
        broker:
        **kwargs:

    Returns: 'RouteEx' request with provided parameters set. No strategy related parameters.

    """

    if service.name() not in request_service_map["GroupRouteEx"]:
        raise ValueError(f"Invalid service received. Service name: {service.name()}")

    request = service.createRequest("GroupRouteEx")

    for seq in order_sequences:
        request.append(EMSX_SEQUENCE, seq)

    # How much% to route and where to
    request.set(EMSX_AMOUNT_PERCENT, amount_percentage)
    request.set(EMSX_BROKER, broker)

    # Below fields are extracted from orders
    # EMSX_HAND_INSTRUCTION
    # EMSX_ORDER_TYPE
    # EMSX_TICKER
    # EMSX_TIF

    # Multi-leg is for options only, implementation skipped here.

    emsx_name_map = {
        "emsx_account"          : EMSX_ACCOUNT,
        "emsx_bookname"         : EMSX_BOOKNAME,
        "emsx_cfd_flag"         : EMSX_CFD_FLAG,
        "emsx_clearing_account" : EMSX_CLEARING_ACCOUNT,
        "emsx_clearing_firm"    : EMSX_CLEARING_FIRM,
        "emsx_exec_instruction" : EMSX_EXEC_INSTRUCTION,
        "emsx_get_warnings"     : EMSX_GET_WARNINGS,
        "emsx_gtd_date"         : EMSX_GTD_DATE,
        "emsx_limit_price"      : EMSX_LIMIT_PRICE,
        "emsx_locate_broker"    : EMSX_LOCATE_BROKER,
        "emsx_locate_id"        : EMSX_LOCATE_ID,
        "emsx_locate_req"       : EMSX_LOCATE_REQ,
        "emsx_notes"            : EMSX_NOTES,
        "emsx_odd_lot"          : EMSX_ODD_LOT,
        "emsx_p_a"              : EMSX_P_A,
        "emsx_release_time"     : EMSX_RELEASE_TIME,
        "emsx_request_seq"      : EMSX_REQUEST_SEQ,
        "emsx_stop_price"       : EMSX_STOP_PRICE,
        "emsx_trader_uuid"      : EMSX_TRADER_UUID
    }

    for param_name, value in kwargs.items():
        if value is None:
            continue

        if emsx_name_map.get(param_name) is None:
            logging.warning(f"Unexpected parameter '{param_name}' provided. Skipping this parameter.")
            continue

        request.set(emsx_name_map[param_name], value)


    return request