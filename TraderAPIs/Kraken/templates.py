import time

templates = {
            "Time":{
                "required": [],
                "scope": "public"
                },
            "SystemStatus":{
                "required": [],
                "scope": "public"
                },
            "Assets":{
                "asset": [],    # NOTE: string
                "aclass": "",   # NOTE: string  # ignore this for now. value only "currency"
                "required": [],
                "scope": "public"
                },
            "AssetPairs":{
                "pair": [], # NOTE: string
                "info": ["info", "leverage", "fees", "margin"], # NOTE: default: info
                "required": [],
                "scope": "public"
                },
            "Ticker":{
                "pair": [], # NOTE: string
                "required": [],
                "scope": "public"
                },
            "OHLC":{
                "pair": [], # NOTE: string  # NOTE: only 1 pair
                "interval": [1, 5, 15, 30, 60, 240, 1440, 10080, 21600],    # Time frame interval in minutes NOTE: default: 1
                "since": (0, int(time.time())),    # Return up to 720 OHLC data points since given timestamp NOTE: timestamp as integer
                "required": ["pair"],
                "scope": "public"
                },
            "Depth":{
                "pair": [], # NOTE: string  # NOTE: only 1 pair
                "count": (1,500),    # Maximum number of asks/bids NOTE: integer between [1..500] default: 100
                "required": ["pair"],
                "scope": "public"
                },
            "Trades":{
                "pair": [], # NOTE: string  # NOTE: only 1 pair
                "since": (0, int(time.time())),    # Return trade data since given timestamp NOTE: timestamp as integer
                "count": (1,1000),    # Return specific number of trades NOTE: integer between [1..1000] default: 1000
                "required": ["pair"],
                "scope": "public"
                },
            "Spread":{
                "pair": [], # NOTE: string  # NOTE: only 1 pair
                "since": (0, int(time.time())),    # Returns spread data since given timestamp. NOTE: timestamp as integer
                "required": ["pair"],
                "scope": "public"
                },
            "Balance":{
                "required": [],
                "scope": "private"
            },
            "BalanceEx":{
                "required": [],
                "scope": "private"
            },
            "TradeBalance":{
                "asset":  [],    # NOTE: string
                "required": [],
                "scope": "private"
            },
            "OpenOrders":{
                "trades": [True, False], # Whether or not to include trades related to position in output
                "userref": (0, 2147483647),  # Restrict results to given user reference id
                "required": [],
                "scope": "private"
            },
            "ClosedOrders":{
                "trades": [True, False], # Whether or not to include trades related to position in output
                "userref": (0, 2147483647),  # Restrict results to given user reference id
                "start": (0, int(time.time())), # Starting unix timestamp or order tx ID of results (exclusive)
                "end": (0, int(time.time())),   # Ending unix timestamp or order tx ID of results (inclusive)
                "ofs": (0, 2147483647), # Result offset for pagination
                "closetime": ["open", "close", "both"], # Which time to use to search # NOTE: default: "both"
                "consolidate_taker": [True, False], # Whether or not to consolidate trades by individual taker trades # NOTE: default: True
                "required": [],
                "scope": "private"
            },
            "QueryOrders":{
                "trades": [True, False], # Whether or not to include trades related to position in output
                "userref": (0, 2147483647),  # Restrict results to given user reference id
                "txid": [], # NOTE: string # Comma delimited list of transaction IDs to query info about (50 maximum)
                "consolidate_taker": [True, False], # Whether or not to consolidate trades by individual taker trades # NOTE: default: True
                "required": ["txid"],
                "scope": "private"
            },
            "TradesHistory":{
                "type": ["all","any position","closed position","closing position","no position"],  # NOTE: default: "all"
                "trades": [True, False],    # Whether or not to include trades related to position in output
                "start": (0, int(time.time())), # Starting unix timestamp or order tx ID of results (exclusive)
                "end": (0, int(time.time())),   # Ending unix timestamp or order tx ID of results (inclusive)
                "ofs": (0, 2147483647), # Result offset for pagination
                "consolidate_taker": [True, False], # Whether or not to consolidate trades by individual taker trades # NOTE: default: True
                "required": [],
                "scope": "private"
            },
            "QueryTrades":{
                "txid": [], # NOTE: string # Comma delimited list of transaction IDs to query info about (50 maximum)
                "trades": [True, False], # Whether or not to include trades related to position in output
                "required": ["txid"],
                "scope": "private"
            },
            "OpenPositions":{
                "txid": [], # NOTE: string # Comma delimited list of transaction IDs to query info about (50 maximum)
                "docalcs": [True, False],   # NOTE: default: False # Whether to include P&L calculations
                "consolidation": ["market"],    # Consolidate positions by market/pair
                "required": [],
                "scope": "private"
            },
            "Ledgers":{
                "asset": [],    # NOTE: string
                "aclass": "",   # NOTE: string  # ignore this for now. value only "currency"
                "type": ["all","deposit","withdrawal","trade","margin","rollover","credit","transfer","settled","staking","sale"],   # NOTE: default: "all" # Type of ledger to retrieve
                "start": (0, int(time.time())), # Starting unix timestamp or order tx ID of results (exclusive)
                "end": (0, int(time.time())),   # Ending unix timestamp or order tx ID of results (inclusive)
                "ofs": (0, 2147483647), # Result offset for pagination
                "without_count": [True, False], # NOTE: default False # If true, does not retrieve count of ledger entries. Request can be noticeably faster for users with many ledger entries as this avoids an extra database query.
                "required": [],
                "scope": "private"
            },
            "QueryLedgers":{
                "id": [],   # Comma delimited list of ledger IDs to query info about (20 maximum)
                "trades": [True, False], # Whether or not to include trades related to position in output
                "required": [],
                "scope": "private"
            },
            "TradeVolume":{
                "pair": [], # NOTE: string
                "required": [],
                "scope": "private"
            },
            "AddExport":{
                "report": ["trades", "ledgers"],
                "format": ["CSV", "TSV"],
                "description": "",
                "fields": ["all", "ordertxid", "time", "ordertype", "price", "cost", "fee", "vol", "margin", "misc", "ledgers", "refid", "type", "aclass", "asset", "amount", "balance"],  # NOTE: default: "all" # trades ->  ordertxid, time, ordertype, price, cost, fee, vol, margin, misc, ledgers # ledgers -> refid, time, type, aclass, asset, amount, fee, balance
                "starttm": (0, int(time.time())),   # NOTE: default: 1st of the current month
                "endtm": (0, int(time.time())), # NOTE: default: now
                "required": ["report", "description"],
                "scope": "private"
            },
            "ExportStatus":{
                "report": ["trades", "ledgers"],    # Type of reports to inquire about
                "required": ["report"],
                "scope": "private"
            },
            "RetrieveExport":{
                "id": "",   # Report ID to retrieve
                "required": ["id"],
                "scope": "private"
            },
            "RemoveExport":{
                "id": "",   # ID of report to delete or cancel
                "type": ["cancel", "delete"],   # delete can only be used for reports that have already been processed. Use cancel for queued or processing reports.
                "required": ["id", "type"],
                "scope": "private"
            }
}   # ToDo:"aclass", "UserTrading", "UserFunding", "User Staking"
