"""
Wrapper function to create 'RouteEx' request without strategy parameters.

As strategy parameters must be appended in the correct order, the parameter input must refer
to the output of `GetBrokerStrategyInfoWithAssetClass` request.
"""

import blpapi
import logging

from dataclasses import dataclass, asdict

from emsx_api_py.requests.request_service_map import request_service_map


# blpapi names
# Mandatory fields
EMSX_SEQUENCE           = blpapi.Name("EMSX_SEQUENCE")
EMSX_AMOUNT             = blpapi.Name("EMSX_AMOUNT")
EMSX_BROKER             = blpapi.Name("EMSX_BROKER")
EMSX_HAND_INSTRUCTION   = blpapi.Name("EMSX_HAND_INSTRUCTION")
EMSX_ORDER_TYPE         = blpapi.Name("EMSX_ORDER_TYPE")
EMSX_TICKER             = blpapi.Name("EMSX_TICKER")
EMSX_TIF                = blpapi.Name("EMSX_TIF")
# Optional fields
EMSX_ACCOUNT            = blpapi.Name("EMSX_ACCOUNT")
EMSX_BOOKNAME           = blpapi.Name("EMSX_BOOKNAME")
EMSX_CFD_FLAG           = blpapi.Name("EMSX_CFD_FLAG")
EMSX_CLEARING_ACCOUNT   = blpapi.Name("EMSX_CLEARING_ACCOUNT")
EMSX_CLEARING_FIRM      = blpapi.Name("EMSX_CLEARING_FIRM")
EMSX_EXEC_INSTRUCTION   = blpapi.Name("EMSX_EXEC_INSTRUCTION")
EMSX_GET_WARNINGS       = blpapi.Name("EMSX_GET_WARNINGS")
EMSX_GTD_DATE           = blpapi.Name("EMSX_GTD_DATE")
EMSX_LIMIT_PRICE        = blpapi.Name("EMSX_LIMIT_PRICE")
EMSX_LOCATE_BROKER      = blpapi.Name("EMSX_LOCATE_BROKER")
EMSX_LOCATE_ID          = blpapi.Name("EMSX_LOCATE_ID")
EMSX_LOCATE_REQ         = blpapi.Name("EMSX_LOCATE_REQ")
EMSX_NOTES              = blpapi.Name("EMSX_NOTES")
EMSX_ODD_LOT            = blpapi.Name("EMSX_ODD_LOT")
EMSX_P_A                = blpapi.Name("EMSX_P_A")
EMSX_RELEASE_TIME       = blpapi.Name("EMSX_RELEASE_TIME")
EMSX_REQUEST_SEQ        = blpapi.Name("EMSX_REQUEST_SEQ")
EMSX_ROUTE_REF_ID       = blpapi.Name("EMSX_ROUTE_REF_ID")
EMSX_STOP_PRICE         = blpapi.Name("EMSX_STOP_PRICE")
EMSX_TRADER_UUID        = blpapi.Name("EMSX_TRADER_UUID")


@dataclass
class RouteExOptionalParams:
    emsx_account         : str | None = None        # "TestAccount"
    emsx_cfd_flag        : bool | None = None       # "0" or "1"
    emsx_clearing_account: str | None = None        # "ClrAccName"
    emsx_clearing_firm   : str | None = None        # "FirmName"
    emsx_exec_instruction: str | None = None        # "AnyInst"
    emsx_get_warnings    : bool | None = None       # "0" or "1"
    emsx_gtd_date        : str | None = None        # "yyyymmdd"
    emsx_limit_price     : float | None = None      # 123.45
    emsx_locate_broker   : str | None = None        # "CLSA"
    emsx_locate_id       : int | None = None        # "SomeID"
    emsx_locate_req      : bool | None = None       # "Y"
    emsx_notes           : str | None = None        # "Some Notes"
    emsx_odd_lot         : bool | None = None       # "0" or "1"
    emsx_p_a             : str | None = None        # "p" or "a"
    emsx_release_time    : str | None = None        # 1259
    emsx_request_seq     : int | None = None        # 1001
    emsx_route_ref_id    : str | None = None        # "UniqueRef"
    emsx_stop_price      : float | None = None      # 123.45
    emsx_trader_uuid     : int | None = None        # 1234567


def route_ex_raw(
        service: blpapi.Service,
        emsx_sequence: int,
        emsx_amount: int,
        emsx_broker: str,
        emsx_order_type: str,       # MKT, LMT, STP, etc. See EMSX API documentation for details.
        emsx_ticker: str,
        emsx_hand_instruction: str = "ANY",
        emsx_tif: str = "DAY",
        # Optional parameters
        optional_params: RouteExOptionalParams = RouteExOptionalParams()
) -> blpapi.Request:

    if service.name not in request_service_map["RouteEx"]:
        raise ValueError(f"Invalid service received. Service name: {service.name()}")

    request = service.createRequest("RouteEx")

    # Mandatory fields
    mandatory_fields = {
        EMSX_SEQUENCE        : emsx_sequence,
        EMSX_AMOUNT          : emsx_amount,
        EMSX_BROKER          : emsx_broker,
        EMSX_HAND_INSTRUCTION: emsx_hand_instruction,
        EMSX_ORDER_TYPE      : emsx_order_type,
        EMSX_TICKER          : emsx_ticker,
        EMSX_TIF             : emsx_tif,
    }

    for field_name, value in mandatory_fields.items():
        request.set(field_name, value)


    # Set optional parameters if provided
    optional_params = asdict(optional_params)
    optional_mapping = {
        "emsx_account"         : EMSX_ACCOUNT,
        "emsx_bookname"        : EMSX_BOOKNAME,
        "emsx_cfd_flag"        : EMSX_CFD_FLAG,
        "emsx_clearing_account": EMSX_CLEARING_ACCOUNT,
        "emsx_clearing_firm"   : EMSX_CLEARING_FIRM,
        "emsx_exec_instruction": EMSX_EXEC_INSTRUCTION,
        "emsx_get_warnings"    : EMSX_GET_WARNINGS,
        "emsx_gtd_date"        : EMSX_GTD_DATE,
        "emsx_limit_price"     : EMSX_LIMIT_PRICE,
        "emsx_locate_broker"   : EMSX_LOCATE_BROKER,
        "emsx_locate_id"       : EMSX_LOCATE_ID,
        "emsx_locate_req"      : EMSX_LOCATE_REQ,
        "emsx_notes"           : EMSX_NOTES,
        "emsx_odd_lot"         : EMSX_ODD_LOT,
        "emsx_p_a"             : EMSX_P_A,
        "emsx_release_time"    : EMSX_RELEASE_TIME,
        "emsx_request_seq"     : EMSX_REQUEST_SEQ,
        "emsx_route_ref_id"    : EMSX_ROUTE_REF_ID,
        "emsx_stop_price"      : EMSX_STOP_PRICE,
        "emsx_trader_uuid"     : EMSX_TRADER_UUID,
    }

    for param_name, value in optional_params.items():
        if value is None:
            continue

        if optional_mapping.get(param_name) is None:
            logging.warning(f"Unexpected parameter '{param_name}' provided. No corresponding RouteEx field found. Skipping this parameter.")
            continue

        request.set(optional_mapping[param_name], value)


    return request