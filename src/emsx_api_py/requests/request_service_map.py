"""
Dictionary = {
    Request: Services that support the request
}
"""


EMSX_HISTORY_PROD_AND_UAT = ("//blp/emsx.history", "//blp/emsx.history.uat")
EMSX_BROKERSPEC_PROD = ("//blp/emsx.brokerspec")
EMAPISVC_PROD_AND_BETA = ("//blp/emapisvc", "//blp/emapisvc_beta")


request_service_map = {
    # //blp/emsx.history
    "GetFills": EMSX_HISTORY_PROD_AND_UAT,
    # //blp/emsx.brokerspec
    "BrokerSpec" : EMSX_BROKERSPEC_PROD,
    # //blp/emapisvc
    # Buy side
    "AssignTrader": EMAPISVC_PROD_AND_BETA,
    "CancelOrderEx": EMAPISVC_PROD_AND_BETA,
    "CancelRoute": EMAPISVC_PROD_AND_BETA,
    "CreateBasket": EMAPISVC_PROD_AND_BETA,
    "CreateOrder": EMAPISVC_PROD_AND_BETA,
    "CreateOrderAndRouteEx": EMAPISVC_PROD_AND_BETA,
    "CreateOrderAndRouteManually": EMAPISVC_PROD_AND_BETA,
    "DeleteOrder": EMAPISVC_PROD_AND_BETA,
    "GetAllFieldMetaData": EMAPISVC_PROD_AND_BETA,
    "GetBrokerStrategiesWithAssetClass": EMAPISVC_PROD_AND_BETA,
    "GetBrokerStrategyInfoWithAssetClass": EMAPISVC_PROD_AND_BETA,
    "GetBrokersWithAssetClass": EMAPISVC_PROD_AND_BETA,
    "GetFieldMetaData": EMAPISVC_PROD_AND_BETA,
    "GetTeams": EMAPISVC_PROD_AND_BETA,
    "GetTradeDesks": EMAPISVC_PROD_AND_BETA,
    "GetTraders": EMAPISVC_PROD_AND_BETA,
    "GroupRouteEx": EMAPISVC_PROD_AND_BETA,
    "ModifyOrderEx": EMAPISVC_PROD_AND_BETA,
    "ModifyRouteEx": EMAPISVC_PROD_AND_BETA,
    "RouteEx": EMAPISVC_PROD_AND_BETA,
    "RouteManuallyEx": EMAPISVC_PROD_AND_BETA,
    # Sell side
    "ManualFill": EMAPISVC_PROD_AND_BETA,
    "SellSideAck": EMAPISVC_PROD_AND_BETA,
    "SellSideReject": EMAPISVC_PROD_AND_BETA,
}