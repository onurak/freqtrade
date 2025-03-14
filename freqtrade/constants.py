# pragma pylint: disable=too-few-public-methods

"""
bot constants
"""
DEFAULT_CONFIG = 'config.json'
DEFAULT_EXCHANGE = 'bittrex'
PROCESS_THROTTLE_SECS = 5  # sec
DEFAULT_TICKER_INTERVAL = 5  # min
HYPEROPT_EPOCH = 100  # epochs
RETRY_TIMEOUT = 30  # sec
DEFAULT_STRATEGY = 'DefaultStrategy'
DEFAULT_HYPEROPT = 'DefaultHyperOpt'
DEFAULT_HYPEROPT_LOSS = 'DefaultHyperOptLoss'
DEFAULT_DB_PROD_URL = 'sqlite:///tradesv3.sqlite'
DEFAULT_DB_DRYRUN_URL = 'sqlite://'
UNLIMITED_STAKE_AMOUNT = 'unlimited'
DEFAULT_AMOUNT_RESERVE_PERCENT = 0.05
REQUIRED_ORDERTIF = ['buy', 'sell']
REQUIRED_ORDERTYPES = ['buy', 'sell', 'stoploss', 'stoploss_on_exchange']
ORDERTYPE_POSSIBILITIES = ['limit', 'market']
ORDERTIF_POSSIBILITIES = ['gtc', 'fok', 'ioc']
AVAILABLE_PAIRLISTS = ['StaticPairList', 'VolumePairList']
DRY_RUN_WALLET = 999.9
MATH_CLOSE_PREC = 1e-14  # Precision used for float comparisons

TICKER_INTERVALS = [
    '1m', '3m', '5m', '15m', '30m',
    '1h', '2h', '4h', '6h', '8h', '12h',
    '1d', '3d', '1w',
]

SUPPORTED_FIAT = [
    "AUD", "BRL", "CAD", "CHF", "CLP", "CNY", "CZK", "DKK",
    "EUR", "GBP", "HKD", "HUF", "IDR", "ILS", "INR", "JPY",
    "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", "PKR", "PLN",
    "RUB", "SEK", "SGD", "THB", "TRY", "TWD", "ZAR", "USD",
    "BTC", "XBT", "ETH", "XRP", "LTC", "BCH", "USDT"
]

MINIMAL_CONFIG = {
    'stake_currency': '',
    'dry_run': True,
    'exchange': {
        'name': '',
        'key': '',
        'secret': '',
        'pair_whitelist': [],
        'ccxt_async_config': {
            'enableRateLimit': True,
        }
    }
}

# Required json-schema for user specified config
CONF_SCHEMA = {
    'type': 'object',
    'properties': {
        'max_open_trades': {'type': 'integer', 'minimum': -1},
        'ticker_interval': {'type': 'string', 'enum': TICKER_INTERVALS},
        'stake_currency': {'type': 'string', 'enum': ['BTC', 'XBT', 'ETH', 'USDT', 'EUR', 'USD']},
        'stake_amount': {
            "type": ["number", "string"],
            "minimum": 0.0005,
            "pattern": UNLIMITED_STAKE_AMOUNT
        },
        'fiat_display_currency': {'type': 'string', 'enum': SUPPORTED_FIAT},
        'dry_run': {'type': 'boolean'},
        'dry_run_wallet': {'type': 'number'},
        'process_only_new_candles': {'type': 'boolean'},
        'minimal_roi': {
            'type': 'object',
            'patternProperties': {
                '^[0-9.]+$': {'type': 'number'}
            },
            'minProperties': 1
        },
        'amount_reserve_percent': {'type': 'number', 'minimum': 0.0, 'maximum': 0.5},
        'stoploss': {'type': 'number', 'maximum': 0, 'exclusiveMaximum': True},
        'trailing_stop': {'type': 'boolean'},
        'trailing_stop_positive': {'type': 'number', 'minimum': 0, 'maximum': 1},
        'trailing_stop_positive_offset': {'type': 'number', 'minimum': 0, 'maximum': 1},
        'trailing_only_offset_is_reached': {'type': 'boolean'},
        'unfilledtimeout': {
            'type': 'object',
            'properties': {
                'buy': {'type': 'number', 'minimum': 3},
                'sell': {'type': 'number', 'minimum': 10}
            }
        },
        'bid_strategy': {
            'type': 'object',
            'properties': {
                'ask_last_balance': {
                    'type': 'number',
                    'minimum': 0,
                    'maximum': 1,
                    'exclusiveMaximum': False,
                    'use_order_book': {'type': 'boolean'},
                    'order_book_top': {'type': 'number', 'maximum': 20, 'minimum': 1},
                    'check_depth_of_market': {
                        'type': 'object',
                        'properties': {
                            'enabled': {'type': 'boolean'},
                            'bids_to_ask_delta': {'type': 'number', 'minimum': 0},
                        }
                    },
                },
            },
            'required': ['ask_last_balance']
        },
        'ask_strategy': {
            'type': 'object',
            'properties': {
                'use_order_book': {'type': 'boolean'},
                'order_book_min': {'type': 'number', 'minimum': 1},
                'order_book_max': {'type': 'number', 'minimum': 1, 'maximum': 50},
                'use_sell_signal': {'type': 'boolean'},
                'sell_profit_only': {'type': 'boolean'},
                'ignore_roi_if_buy_signal': {'type': 'boolean'}
            }
        },
        'order_types': {
            'type': 'object',
            'properties': {
                'buy': {'type': 'string', 'enum': ORDERTYPE_POSSIBILITIES},
                'sell': {'type': 'string', 'enum': ORDERTYPE_POSSIBILITIES},
                'emergencysell': {'type': 'string', 'enum': ORDERTYPE_POSSIBILITIES},
                'stoploss': {'type': 'string', 'enum': ORDERTYPE_POSSIBILITIES},
                'stoploss_on_exchange': {'type': 'boolean'},
                'stoploss_on_exchange_interval': {'type': 'number'}
            },
            'required': ['buy', 'sell', 'stoploss', 'stoploss_on_exchange']
        },
        'order_time_in_force': {
            'type': 'object',
            'properties': {
                'buy': {'type': 'string', 'enum': ORDERTIF_POSSIBILITIES},
                'sell': {'type': 'string', 'enum': ORDERTIF_POSSIBILITIES}
            },
            'required': ['buy', 'sell']
        },
        'exchange': {'$ref': '#/definitions/exchange'},
        'edge': {'$ref': '#/definitions/edge'},
        'experimental': {
            'type': 'object',
            'properties': {
                'use_sell_signal': {'type': 'boolean'},
                'sell_profit_only': {'type': 'boolean'},
                'ignore_roi_if_buy_signal': {'type': 'boolean'},
                'block_bad_exchanges': {'type': 'boolean'}
            }
        },
        'pairlist': {
            'type': 'object',
            'properties': {
                'method': {'type': 'string', 'enum': AVAILABLE_PAIRLISTS},
                'config': {'type': 'object'}
            },
            'required': ['method']
        },
        'telegram': {
            'type': 'object',
            'properties': {
                'enabled': {'type': 'boolean'},
                'token': {'type': 'string'},
                'chat_id': {'type': 'string'},
            },
            'required': ['enabled', 'token', 'chat_id']
        },
        'webhook': {
            'type': 'object',
            'properties': {
                'enabled': {'type': 'boolean'},
                'webhookbuy': {'type': 'object'},
                'webhooksell': {'type': 'object'},
                'webhookstatus': {'type': 'object'},
            },
        },
        'api_server': {
            'type': 'object',
            'properties': {
                'enabled': {'type': 'boolean'},
                'listen_ip_address': {'format': 'ipv4'},
                'listen_port': {
                    'type': 'integer',
                    "minimum": 1024,
                    "maximum": 65535
                },
                'username': {'type': 'string'},
                'password': {'type': 'string'},
            },
            'required': ['enabled', 'listen_ip_address', 'listen_port', 'username', 'password']
        },
        'db_url': {'type': 'string'},
        'initial_state': {'type': 'string', 'enum': ['running', 'stopped']},
        'forcebuy_enable': {'type': 'boolean'},
        'internals': {
            'type': 'object',
            'properties': {
                'process_throttle_secs': {'type': 'number'},
                'interval': {'type': 'integer'},
                'sd_notify': {'type': 'boolean'},
            }
        }
    },
    'definitions': {
        'exchange': {
            'type': 'object',
            'properties': {
                'name': {'type': 'string'},
                'sandbox': {'type': 'boolean', 'default': False},
                'key': {'type': 'string', 'default': ''},
                'secret': {'type': 'string', 'default': ''},
                'password': {'type': 'string', 'default': ''},
                'uid': {'type': 'string'},
                'pair_whitelist': {
                    'type': 'array',
                    'items': {
                        'type': 'string',
                        'pattern': '^[0-9A-Z]+/[0-9A-Z]+$'
                    },
                    'uniqueItems': True
                },
                'pair_blacklist': {
                    'type': 'array',
                    'items': {
                        'type': 'string',
                        'pattern': '^[0-9A-Z]+/[0-9A-Z]+$'
                    },
                    'uniqueItems': True
                },
                'outdated_offset': {'type': 'integer', 'minimum': 1},
                'markets_refresh_interval': {'type': 'integer'},
                'ccxt_config': {'type': 'object'},
                'ccxt_async_config': {'type': 'object'}
            },
            'required': ['name']
        },
        'edge': {
            'type': 'object',
            'properties': {
                "enabled": {'type': 'boolean'},
                "process_throttle_secs": {'type': 'integer', 'minimum': 600},
                "calculate_since_number_of_days": {'type': 'integer'},
                "allowed_risk": {'type': 'number'},
                "capital_available_percentage": {'type': 'number'},
                "stoploss_range_min": {'type': 'number'},
                "stoploss_range_max": {'type': 'number'},
                "stoploss_range_step": {'type': 'number'},
                "minimum_winrate": {'type': 'number'},
                "minimum_expectancy": {'type': 'number'},
                "min_trade_number": {'type': 'number'},
                "max_trade_duration_minute": {'type': 'integer'},
                "remove_pumps": {'type': 'boolean'}
            },
            'required': ['process_throttle_secs', 'allowed_risk', 'capital_available_percentage']
        }
    },
    'anyOf': [
        {'required': ['exchange']}
    ],
    'required': [
        'max_open_trades',
        'stake_currency',
        'stake_amount',
        'dry_run',
        'bid_strategy',
        'unfilledtimeout',
    ]
}
