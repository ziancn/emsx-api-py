"""
Wrapper method to create 'CreateOrderAndRouteEx' request.
No strategy parameters are set or included.
"""

import blpapi
import logging

from typing import TypedDict, Unpack, NotRequired

from .create_basket import EMSX_BASKET_NAME
from ..request_service_map import request_service_map


# blpapi names
# Mandatory parameters
EMSX_TICKER           = blpapi.Name("EMSX_TICKER")
EMSX_AMOUNT           = blpapi.Name("EMSX_AMOUNT")
EMSX_ORDER_TYPE       = blpapi.Name("EMSX_ORDER_TYPE")
EMSX_TIF              = blpapi.Name("EMSX_TIF")
EMSX_HAND_INSTRUCTION = blpapi.Name("EMSX_HAND_INSTRUCTION")
EMSX_SIDE             = blpapi.Name("EMSX_SIDE")
# Optional parameters
EMSX_ACCOUNT              = blpapi.Name("EMSX_ACCOUNT")
EMSX_BOOKNAME             = blpapi.Name("EMSX_BOOKNAME")
EMSX_BROKER               = blpapi.Name("EMSX_BROKER")
EMSX_CFD_FLAG             = blpapi.Name("EMSX_CFD_FLAG")
EMSX_CLEARING_ACCOUNT     = blpapi.Name("EMSX_CLEARING_ACCOUNT")
EMSX_CLEARING_FIRM        = blpapi.Name("EMSX_CLEARING_FIRM")
EMSX_CUSTOM_NOTE1         = blpapi.Name("EMSX_CUSTOM_NOTE1")
EMSX_CUSTOM_NOTE2         = blpapi.Name("EMSX_CUSTOM_NOTE2")
EMSX_CUSTOM_NOTE3         = blpapi.Name("EMSX_CUSTOM_NOTE3")
EMSX_CUSTOM_NOTE4         = blpapi.Name("EMSX_CUSTOM_NOTE4")
EMSX_CUSTOM_NOTE5         = blpapi.Name("EMSX_CUSTOM_NOTE5")
EMSX_EXCHANGE_DESTINATION = blpapi.Name("EMSX_EXCHANGE_DESTINATION")
EMSX_EXEC_INSTRUCTION     = blpapi.Name("EMSX_EXEC_INSTRUCTION")
EMSX_GET_WARNINGS         = blpapi.Name("EMSX_GET_WARNINGS")
EMSX_GTD_DATE             = blpapi.Name("EMSX_GTD_DATE")
EMSX_INVESTOR_ID          = blpapi.Name("EMSX_INVESTOR_ID")
EMSX_LIMIT_PRICE          = blpapi.Name("EMSX_LIMIT_PRICE")
EMSX_LOCATE_BROKER        = blpapi.Name("EMSX_LOCATE_BROKER")
EMSX_LOCATE_ID            = blpapi.Name("EMSX_LOCATE_ID")
EMSX_LOCATE_REQ           = blpapi.Name("EMSX_LOCATE_REQ")
EMSX_NOTES                = blpapi.Name("EMSX_NOTES")
EMSX_ODD_LOT              = blpapi.Name("EMSX_ODD_LOT")
EMSX_ORDER_ORIGIN         = blpapi.Name("EMSX_ORDER_ORIGIN")
EMSX_ORDER_REF_ID         = blpapi.Name("EMSX_ORDER_REF_ID")
EMSX_P_A                  = blpapi.Name("EMSX_P_A")
EMSX_RELEASE_TIME         = blpapi.Name("EMSX_RELEASE_TIME")
EMSX_REQUEST_SEQ          = blpapi.Name("EMSX_REQUEST_SEQ")
EMSX_ROUTE_REF_ID         = blpapi.Name("EMSX_ROUTE_REF_ID")
EMSX_SETTLE_CURRENCY      = blpapi.Name("EMSX_SETTLE_CURRENCY")
EMSX_SETTLE_DATE          = blpapi.Name("EMSX_SETTLE_DATE")
EMSX_SETTLE_TYPE          = blpapi.Name("EMSX_SETTLE_TYPE")
EMSX_STOP_PRICE           = blpapi.Name("EMSX_STOP_PRICE")


# Optional parameters
class CreateOrderAndRouteExOptional(TypedDict, total=False):
    emsx_account              : NotRequired[str]        # "TestAccount"
    emsx_bookname             : NotRequired[str]        # "BookName"
    emsx_basket_name          : NotRequired[str]        # "BasketName"
    emsx_cfd_flag             : NotRequired[str]        # "0" or "1"
    emsx_clearing_account     : NotRequired[str]        # "ClrAccName"
    emsx_clearing_firm        : NotRequired[str]        # "FirmName"
    emsx_custom_note1         : NotRequired[str]
    emsx_custom_note2         : NotRequired[str]
    emsx_custom_note3         : NotRequired[str]
    emsx_custom_note4         : NotRequired[str]
    emsx_custom_note5         : NotRequired[str]
    emsx_exchange_destination : NotRequired[str]        # "XSHG"
    emsx_exec_instruction     : NotRequired[str]        # "AnyInst"
    emsx_get_warnings         : NotRequired[str]        # "0" or "1"
    emsx_gtd_date             : NotRequired[str]        # "yyyymmdd"
    emsx_investor_id          : NotRequired[str]        # "InvID"
    emsx_limit_price          : NotRequired[float]      # 123.45
    emsx_locate_broker        : NotRequired[str]        # "CLSA"
    emsx_locate_id            : NotRequired[int]        # "SomeID"
    emsx_locate_req           : NotRequired[str]        # "Y"
    emsx_notes                : NotRequired[str]        # "Some notes about the order"
    emsx_odd_lot              : NotRequired[str]        # "0" or "1"
    emsx_order_origin         : NotRequired[str]        # ""
    emsx_order_ref_id         : NotRequired[str]        # "UniqueID"
    emsx_p_a                  : NotRequired[str]        # "0" or "1"
    emsx_release_time         : NotRequired[str]        # "yyyymmdd-HH:MM:SS"
    emsx_request_seq          : NotRequired[int]        # 12345
    emsx_route_ref_id         : NotRequired[str]        # "SomeID"
    emsx_settle_currency      : NotRequired[str]        # "USD"
    emsx_settle_date          : NotRequired[int]        # 20260226
    emsx_settle_type          : NotRequired[str]        # "T+2"
    emsx_stop_price           : NotRequired[float]      # 123.45


def create_order_and_route_ex_raw(
        service: blpapi.Service,
        *,
        emsx_ticker: str,
        emsx_amount: int,
        emsx_order_type: str,  # MKT, LMT, etc.
        emsx_side: str,        # BUY, SELL, SHRT, COVR, B/O, B/C, S/O, S/C
        emsx_broker: str,
        emsx_tif: str = "DAY",
        emsx_hand_instruction: str = "ANY",
        # Optional parameters
        **kwargs: Unpack[CreateOrderAndRouteExOptional]
) -> blpapi.Request:
    """

    Args:
        service:
        emsx_ticker:
        emsx_amount:
        emsx_order_type:
        emsx_side:
        emsx_broker:
        emsx_tif:
        emsx_hand_instruction:
        **kwargs:

    Returns:

    """
    if service.name() not in request_service_map["CreateOrderAndRouteEx"]:
        raise ValueError(f"Invalid service received. Service name: {service.name()}")

    request = service.createRequest("CreateOrderAndRouteEx")


    # Mandatory parameters
    mandatory_params = {
        EMSX_TICKER: emsx_ticker,
        EMSX_AMOUNT: emsx_amount,
        EMSX_ORDER_TYPE: emsx_order_type,
        EMSX_SIDE: emsx_side,
        EMSX_BROKER: emsx_broker,
        EMSX_TIF: emsx_tif,
        EMSX_HAND_INSTRUCTION: emsx_hand_instruction
    }

    for field, value in mandatory_params.items():
        request.set(field, value)


    # Optional params
    emsx_name_map = {
        "emsx_account"              : EMSX_ACCOUNT,
        "emsx_bookname"             : EMSX_BOOKNAME,
        "emsx_basket_name"          : EMSX_BASKET_NAME,
        "emsx_cfd_flag"             : EMSX_CFD_FLAG,
        "emsx_clearing_account"     : EMSX_CLEARING_ACCOUNT,
        "emsx_clearing_firm"        : EMSX_CLEARING_FIRM,
        "emsx_custom_note1"         : EMSX_CUSTOM_NOTE1,
        "emsx_custom_note2"         : EMSX_CUSTOM_NOTE2,
        "emsx_custom_note3"         : EMSX_CUSTOM_NOTE3,
        "emsx_custom_note4"         : EMSX_CUSTOM_NOTE4,
        "emsx_custom_note5"         : EMSX_CUSTOM_NOTE5,
        "emsx_exchange_destination" : EMSX_EXCHANGE_DESTINATION,
        "emsx_exec_instruction"     : EMSX_EXEC_INSTRUCTION,
        "emsx_get_warnings"         : EMSX_GET_WARNINGS,
        "emsx_gtd_date"             : EMSX_GTD_DATE,
        "emsx_investor_id"          : EMSX_INVESTOR_ID,
        "emsx_limit_price"          : EMSX_LIMIT_PRICE,
        "emsx_locate_broker"        : EMSX_LOCATE_BROKER,
        "emsx_locate_id"            : EMSX_LOCATE_ID,
        "emsx_locate_req"           : EMSX_LOCATE_REQ,
        "emsx_notes"                : EMSX_NOTES,
        "emsx_odd_lot"              : EMSX_ODD_LOT,
        "emsx_order_origin"         : EMSX_ORDER_ORIGIN,
        "emsx_order_ref_id"         : EMSX_ORDER_REF_ID,
        "emsx_p_a"                  : EMSX_P_A,
        "emsx_release_time"         : EMSX_RELEASE_TIME,
        "emsx_request_seq"          : EMSX_REQUEST_SEQ,
        "emsx_route_ref_id"         : EMSX_ROUTE_REF_ID,
        "emsx_settle_currency"      : EMSX_SETTLE_CURRENCY,
        "emsx_settle_date"          : EMSX_SETTLE_DATE,
        "emsx_settle_type"          : EMSX_SETTLE_TYPE,
        "emsx_stop_price"           : EMSX_STOP_PRICE,
    }

    for param_name, value in kwargs.items():
        if value is None:
            continue

        if emsx_name_map.get(param_name) is None:
            logging.warning(f"Unexpected parameter '{param_name}' provided. Skipping this parameter.")
            continue

        request.set(emsx_name_map[param_name], value)


    return request