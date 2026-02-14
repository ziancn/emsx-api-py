"""
Collection of service names for Bloomberg APIs
"""


# === Standard EMSX service for subscription and request-response ===
EMAPISVC      = "//blp/emapisvc"
EMAPISVC_BETA = "//blp/emapisvc_beta"


# === EMSX historical data service ===
EMSX_HISTORY     = "//blp/emsx.history"
EMSX_HISTORY_UAT = "//blp/emsx.history.uat"


# === EMSX Broker strategy specifics ===
EMSX_BROKERSPEC = "//blp/emsx.brokerspec"


# === (Server-side) Authentication ===
APIAUTH = "//blp/apiauth"


# === Bloomberg generic services ===
MKTDATA = "//blp/mktdata"   # Real-time market data
REFDATA = "//blp/refdata"   # Static reference data