from typing import List, Optional, TYPE_CHECKING
from typing import cast as typecast

from multi import multi
from ...ir.irlistener import IRListener
from ...ir.irfilter import IRFilter

from .v2tls import V2TLSContext
from .v2route import V2Route

if TYPE_CHECKING:
    from . import V2Config


class V2Bootstrap(dict):
    def __init__(self, config: 'V2Config') -> None:
        super().__init__(**{
            "node": {
                "cluster": "ignored",
                "id": "test-id"     # MUST BE test-id, see below
            },
            "static_resources": {
                "clusters": [ {
                    "name": "xds_cluster",
                    "connect_timeout": "1s",
                    "hosts": [ {
                        "socket_address": {
                            "address": "127.0.0.1",
                            "port_value": 18000
                        }
                    }],
                    "http2_protocol_options": {}
                } ]
            },
            "dynamic_resources": {
                "ads_config": {
                    "api_type": "GRPC",
                    "grpc_services": [ {
                        "envoy_grpc": {
                            "cluster_name": "xds_cluster"
                        }
                    } ]
                },
                "cds_config": { "ads": {} },
                "lds_config": { "ads": {} }
            },
            "admin": dict(config.admin)
        })

        if config.tracing:
            self['tracing'] = dict(config.tracing)


    @classmethod
    def generate(cls, config: 'V2Config') -> 'V2Bootstrap':
        # Should we save this?
        config.bootstrap = V2Bootstrap(config)
