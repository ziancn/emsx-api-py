"""
This module automates routing EMSX blotter incoming Korean Stock orders to CLET (CLSA IE)
"""

import blpapi
import logging

from win11toast import notify

from emsx_api_py.modules import ModuleProtocol
from emsx_api_py.requests.buyside import route_ex_raw
from emsx_api_py.requests import append_strategy


# blpapi names
MSG_SUB_TYPE = blpapi.Name("MSG_SUB_TYPE")
EMSX_EXCHANGE = blpapi.Name("EMSX_EXCHANGE")
EMSX_TRADER = blpapi.Name("EMSX_TRADER")
EMSX_SIDE = blpapi.Name("EMSX_SIDE")
EMSX_TICKER = blpapi.Name("EMSX_TICKER")
EMSX_AMOUNT = blpapi.Name("EMSX_AMOUNT")
EMSX_NOTES = blpapi.Name("EMSX_NOTES")
EMSX_STATUS = blpapi.Name("EMSX_STATUS")
EMSX_ACCOUNT = blpapi.Name("EMSX_ACCOUNT")
EMSX_ORDER_TYPE = blpapi.Name("EMSX_ORDER_TYPE")
EMSX_SEQUENCE = blpapi.Name("EMSX_SEQUENCE")
EMSX_LIMIT_PRICE = blpapi.Name("EMSX_LIMIT_PRICE")


EMSX_STRATEGY_PARAMS = blpapi.Name("EMSX_STRATEGY_PARAMS")
EMSX_STRATEGY_NAME = blpapi.Name("EMSX_STRATEGY_NAME")
EMSX_STRATEGY_FIELD_INDICATORS = blpapi.Name("EMSX_STRATEGY_FIELD_INDICATORS")
EMSX_STRATEGY_FIELDS = blpapi.Name("EMSX_STRATEGY_FIELDS")
EMSX_FIELD_DATA = blpapi.Name("EMSX_FIELD_DATA")
EMSX_FIELD_INDICATOR = blpapi.Name("EMSX_FIELD_INDICATOR")


# Subscription fields
ORDER_SUB_FIELDS = [
    "EMSX_SEQUENCE",
    "EMSX_TRADER",
    "EMSX_ACCOUNT",
    "EMSX_SIDE",
    "EMSX_ORDER_TYPE",
    "EMSX_TICKER",
    "EMSX_EXCHANGE",
    "EMSX_AMOUNT",
    "EMSX_STATUS",
    "EMSX_NOTES",
    "EMSX_LIMIT_PRICE",
]

ROUTE_SUB_FIELDS = [
    "API_SEQ_NUM",
    # "EMSX_AMOUNT",
    # "EMSX_AVG_PRICE",
    # "EMSX_BROKER",
    # "EMSX_BROKER_COMM",
    # "EMSX_BSE_AVG_PRICE",
    # "EMSX_BSE_FILLED",
    # "EMSX_BROKER_STATUS",
    # "EMSX_CLEARING_ACCOUNT",
    # "EMSX_CLEARING_FIRM",
    # "EMSX_COMM_DIFF_FLAG",
    # "EMSX_COMM_RATE",
    # "EMSX_CURRENCY_PAIR",
    # "EMSX_CUSTOM_ACCOUNT",
    # "EMSX_DAY_AVG_PRICE",
    # "EMSX_DAY_FILL",
    # "EMSX_EXCHANGE_DESTINATION",
    # "EMSX_EXEC_INSTRUCTION",
    # "EMSX_EXECUTE_BROKER",
    # "EMSX_FILL_ID",
    # "EMSX_FILLED",
    # "EMSX_GTD_DATE",
    # "EMSX_HAND_INSTRUCTION",
    # "EMSX_IS_MANUAL_ROUTE",
    # "EMSX_LAST_FILL_DATE",
    # "EMSX_LAST_FILL_TIME",
    # "EMSX_LAST_MARKET",
    # "EMSX_LAST_PRICE",
    # "EMSX_LAST_SHARES",
    # "EMSX_LIMIT_PRICE",
    # "EMSX_MISC_FEES",
    # "EMSX_ML_LEG_QUANTITY",
    # "EMSX_ML_NUM_LEGS",
    # "EMSX_ML_PERCENT_FILLED",
    # "EMSX_ML_RATIO",
    # "EMSX_ML_REMAIN_BALANCE",
    # "EMSX_ML_STRATEGY",
    # "EMSX_ML_TOTAL_QUANTITY",
    # "EMSX_NOTES",
    # "EMSX_NSE_AVG_PRICE",
    # "EMSX_NSE_FILLED",
    # "EMSX_ORDER_TYPE",
    # "EMSX_P_A",
    # "EMSX_PERCENT_REMAIN",
    # "EMSX_PRINCIPAL",
    # "EMSX_QUEUED_DATE",
    # "EMSX_QUEUED_TIME",
    # "EMSX_REASON_CODE",
    # "EMSX_REASON_DESC",
    # "EMSX_REMAIN_BALANCE",
    # "EMSX_ROUTE_CREATE_DATE",
    # "EMSX_ROUTE_CREATE_TIME",
    # "EMSX_ROUTE_ID",
    # "EMSX_ROUTE_LAST_UPDATE_TIME",
    # "EMSX_ROUTE_PRICE",
    # "EMSX_SEQUENCE",
    # "EMSX_SETTLE_AMOUNT",
    # "EMSX_SETTLE_DATE",
    # "EMSX_STATUS",
    # "EMSX_STOP_PRICE",
    # "EMSX_STRATEGY_END_TIME",
    # "EMSX_STRATEGY_PART_RATE1",
    # "EMSX_STRATEGY_PART_RATE2",
    # "EMSX_STRATEGY_START_TIME",
    # "EMSX_STRATEGY_STYLE",
    # "EMSX_STRATEGY_TYPE",
    # "EMSX_TIF",
    # "EMSX_TIME_STAMP",
    # "EMSX_TYPE",
    # "EMSX_URGENCY_LEVEL",
    # "EMSX_USER_COMM_AMOUNT",
    # "EMSX_USER_COMM_RATE",
    # "EMSX_USER_FEES",
    # "EMSX_USER_NET_MONEY",
    # "EMSX_ROUTE_AS_OF_DATE",
    # "EMSX_WORKING",
]


class KoreaAutoRoute(ModuleProtocol):
    def __init__(self):
        self._order_sub_cid = blpapi.CorrelationId(98)
        self._route_sub_cid = blpapi.CorrelationId(99)
        self._request_cids = []


    def process_event(
            self,
            event  : blpapi.Event,
            session: blpapi.Session,
    ):
        et = event.eventType()
        match et:
            case blpapi.Event.SESSION_STATUS    : self.process_session_status_event(event, session)
            case blpapi.Event.SERVICE_STATUS    : self.process_service_status_event(event, session)
            case blpapi.Event.SUBSCRIPTION_DATA : self.process_subscription_data_event(event, session)
            case blpapi.Event.RESPONSE          : self.process_response(event, session)
            case blpapi.Event.PARTIAL_RESPONSE  : self.process_response(event, session)
            case _: pass


    """SESSION EVENT PROCESSING"""
    @staticmethod
    def process_session_status_event(event: blpapi.Event, session: blpapi.Session):
        for msg in event:
            if msg.messageType() == blpapi.Name("SessionStarted"):
                session.openServiceAsync("//blp/emapisvc")

    def process_service_status_event(self, event: blpapi.Event, session: blpapi.Session):
        for msg in event:
            if msg.messageType() == blpapi.Name("ServiceOpened"):
                self._subscribe_orders(session)
                self._subscribe_routes(session)

    def _subscribe_orders(self, session: blpapi.Session):
        topic = "//blp/emapisvc/order;team=CITICHK?fields=" + ",".join(ORDER_SUB_FIELDS)
        subscription = blpapi.SubscriptionList()
        subscription.add(topic=topic, correlationId=self._order_sub_cid)
        session.subscribe(subscription)

    def _subscribe_routes(self, session: blpapi.Session):
        topic = "//blp/emapisvc/route;team=CITICHK?fields=" + ",".join(ROUTE_SUB_FIELDS)
        subscription = blpapi.SubscriptionList()
        subscription.add(topic=topic, correlationId=self._route_sub_cid)
        session.subscribe(subscription)

    def process_subscription_data_event(self, event: blpapi.Event, session: blpapi.Session):
        for msg in event:
            try:
                if msg.messageType() != blpapi.Name("OrderRouteFields"): continue
                match msg.getElementAsInteger("EVENT_STATUS"):
                    case 1  : self._log_heartbeat(msg)
                    case 11 : self._log_initial_paint(msg)
                    case 6  : self._process_event_6(msg, session)  # new order or route
                    case 7  : self._process_event_7(msg, session)  # update order or route
            except Exception as e:
                logging.exception(f"[{self.__class__.__name__}] Exception: {e}")

    def process_response(self, event: blpapi.Event, session: blpapi.Session):
        """Just log first, no handling logics as of now"""
        for msg in event:
            if msg.correlationIds()[0] not in self._request_cids: continue
            else: print(msg)

    def _log_heartbeat(self, msg: blpapi.Message):
        if msg.correlationIds()[0].value() == self._order_sub_cid.value():
            logging.info("O.")
        elif msg.correlationIds()[0].value() == self._route_sub_cid.value():
            logging.info("R.")

    def _log_initial_paint(self, msg: blpapi.Message):
        if msg.correlationIds()[0].value() == self._order_sub_cid.value():
            logging.info("Order - End of initial paint")
        elif msg.correlationIds()[0].value() == self._route_sub_cid.value():
            logging.info("Route - End of initial paint")



    """ROUTING EVENTS HANDLING AND LOGICS"""
    def _process_event_6(self, msg: blpapi.Message, session: blpapi.Session):
        if not msg.hasElement(MSG_SUB_TYPE):
            return

        match msg.getElementAsString(MSG_SUB_TYPE):
            case "O": self._process_new_order(msg, session)
            case "R": self._process_new_route(msg, session)

    def _process_new_order(self, msg: blpapi.Message, session: blpapi.Session):
        # === Check if is target order ===
        if not self._is_target_order(msg): return
        # === Log incoming target order ===
        self._log_korean_order(msg)
        # === Routing Logic ===
        side = msg.getElementAsString(EMSX_SIDE) if msg.hasElement(EMSX_SIDE) else "N/A"
        match side:
            case "SELL" : self._process_sell_order(msg, session)
            case "BUY"  : self._process_buy_order(msg, session)
            case _: logging.warning(f"[{self.__class__.__name__}] Unrecognized EMSX_SIDE: {side}")

    def _process_new_route(self, msg: blpapi.Message, session: blpapi.Session):
        # logging.info(f"New route event handler not implemented yet.")
        ...

    @staticmethod
    def _is_target_order(msg: blpapi.Message):
        exch   = msg.getElementAsString(EMSX_EXCHANGE) if msg.hasElement(EMSX_EXCHANGE) else "N/A"
        trader = msg.getElementAsString(EMSX_TRADER)   if msg.hasElement(EMSX_TRADER)   else "N/A"
        notes  = msg.getElementAsString(EMSX_NOTES)    if msg.hasElement(EMSX_NOTES)    else "N/A"

        return (exch == "KS" and                        # Korean exchange sym
                trader == "YOURTARGETTRADER" and        # Target assigned trader
                "@" in notes)                           # "@" separator in notes

    def _log_korean_order(self, msg: blpapi.Message):
        trader     = msg.getElementAsString(EMSX_TRADER)     if msg.hasElement(EMSX_TRADER)      else "N/A"
        notes      = msg.getElementAsString(EMSX_NOTES)      if msg.hasElement(EMSX_NOTES)       else "N/A"
        side       = msg.getElementAsString(EMSX_SIDE)       if msg.hasElement(EMSX_SIDE)        else "N/A"
        ticker     = msg.getElementAsString(EMSX_TICKER)     if msg.hasElement(EMSX_TICKER)      else "N/A"
        qty        = msg.getElementAsInteger(EMSX_AMOUNT)    if msg.hasElement(EMSX_AMOUNT)      else 0
        status     = msg.getElementAsString(EMSX_STATUS)     if msg.hasElement(EMSX_STATUS)      else "N/A"
        account    = msg.getElementAsString(EMSX_ACCOUNT)    if msg.hasElement(EMSX_ACCOUNT)     else "N/A"
        order_type = msg.getElementAsString(EMSX_ORDER_TYPE) if msg.hasElement(EMSX_ORDER_TYPE)  else "N/A"
        lmt_price  = msg.getElementAsFloat(EMSX_LIMIT_PRICE) if msg.hasElement(EMSX_LIMIT_PRICE) else 0.
        # Parse strategy and params
        algo_name, algo_start_time, algo_end_time, algo_max_vol_str, *_ = notes.split("@")
        algo_max_vol = float(algo_max_vol_str) if algo_max_vol_str else 0


        logging.info(
            f"[{self.__class__.__name__}] NEW KS ORDER:\n"
            f"  ==================\n"
            f"  Trader  : {trader}\n"
            f"  Account : {account}\n"
            f"  Side    : {side}\n"
            f"  Type    : {order_type}\n"
            f"  Lmt Px  : {lmt_price}\n"
            f"  Qty     : {qty:,}\n"
            f"  Ticker  : {ticker}\n"
            f"  Status  : {status}\n"
            f"  Seq#    : {msg.getElementAsInteger(EMSX_SEQUENCE) if msg.hasElement(EMSX_SEQUENCE) else 'N/A'}\n"
            f"  Notes   : {notes}\n"
            f"  ==================\n"
            f"  Algo Parameters\n"
            f"  Algo name  : {algo_name}\n"
            f"  Start time : {algo_start_time}\n"
            f"  End time   : {algo_end_time}\n"
            f"  Vol cap%   : {algo_max_vol}\n"
            f"  =================="
        )

    def _process_sell_order(self, msg: blpapi.Message, session: blpapi.Session):
        """We don't process SELL as of now, just send a notification"""
        notify(title="NEW KR EQTY SELL ORDER", body="Please route manually", button="Dismiss", scenario="reminder")

    def _process_buy_order(self, msg: blpapi.Message, session: blpapi.Session):
        # Parse
        ticker     = msg.getElementAsString(EMSX_TICKER)     if msg.hasElement(EMSX_TICKER)      else "N/A"
        qty        = msg.getElementAsInteger(EMSX_AMOUNT)    if msg.hasElement(EMSX_AMOUNT)      else 0
        sequence   = msg.getElementAsInteger(EMSX_SEQUENCE)  if msg.hasElement(EMSX_SEQUENCE)    else "N/A"
        order_type = msg.getElementAsString(EMSX_ORDER_TYPE) if msg.hasElement(EMSX_ORDER_TYPE)  else "N/A"
        lmt_price  = msg.getElementAsFloat(EMSX_LIMIT_PRICE) if msg.hasElement(EMSX_LIMIT_PRICE) else 0.
        notes      = msg.getElementAsString(EMSX_NOTES)      if msg.hasElement(EMSX_NOTES)       else "N/A"
        # Parse strategy and params
        strategy_name, strategy_start_time, strategy_end_time, strategy_max_vol_str, *_ = notes.split("@")
        strategy_max_vol = float(strategy_max_vol_str) if strategy_max_vol_str else 0
        # Draft RouteEx request
        route_request = route_ex_raw(
            session.getService("//blp/emapisvc"),
            emsx_sequence=sequence,
            emsx_amount=qty,
            emsx_broker="CLET",
            emsx_order_type=order_type,
            emsx_ticker=ticker,
            emsx_hand_instruction="MAN",
            emsx_limit_price=lmt_price if order_type == "LMT" else None,
            emsx_account="CHD1 RISK",
            emsx_trader_uuid=12345678  # Order owner's uuid if you route on behalf
        )
        # Instruction Alog Name -> CLET Algo Name
        algo_map = {
            "OneOrder": "VolinLine",  # For execution safety, we use POV to hedge all DMA
            "POV"     : "VolinLine",
            "TWAP"    : "TWAP_ADP",
            "VWAP"    : "VWAP_ADP"
        }

        clet_algo_name = algo_map.get(strategy_name)
        if clet_algo_name is None:
            notify("NEW KS BUY ORDER - Unsupported Algo",
                   "Please check manually",
                   button="Dismiss", scenario="reminder")
            return

        match clet_algo_name:
            case "DMA":
                pass # There is no DMA in our case
            case "VolinLine":
                # If this "VolinLine" is mapping from "OneOrder", we fill POV25% by default
                max_vol_input = 25 if strategy_name == "OneOrder" else strategy_max_vol

                params = [(strategy_start_time, 0 if strategy_start_time else 1),   # Start Time
                          (strategy_end_time  , 0 if strategy_end_time   else 1),   # End Time
                          (""                 , 1                              ),   # AuctPartRate
                          (0                  , 1                              ),   # Min%Volume
                          (max_vol_input      , 0                              )]   # Max%Volume


                append_strategy(route_request, clet_algo_name, params)

            case _: # VWAP TWAP
                params = [(strategy_start_time, 0 if strategy_start_time else 1),   # Start Time
                          (strategy_end_time  , 0 if strategy_end_time   else 1),   # End Time
                          (""                 , 1                              ),   # AuctPartRate
                          (strategy_max_vol   , 0 if strategy_max_vol    else 1)]   # Max%Volume


                append_strategy(route_request, clet_algo_name, params)

        cid = blpapi.CorrelationId()
        session.sendRequest(route_request, correlationId=cid)
        self._request_cids.append(cid)
        # print(route_request.toString())
        logging.info(f"ATTENTION: Auto-routed!")


    def _process_event_7(self, msg: blpapi.Message, session: blpapi.Session):
        # logging.info("Event status 7 handler not implemented yet.")
        ...