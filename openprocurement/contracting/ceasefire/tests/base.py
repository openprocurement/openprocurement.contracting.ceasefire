from openprocurement.contracting.core.tests.base import BaseWebTest as CoreBaseWebTest

from os import path
from openprocurement.contracting.core.tests.base import (
    MOCK_CONFIG as BASE_MOCK_CONFIG,
    connection_mock_config
)
from openprocurement.contracting.ceasefire.tests.fixtures.config import PARTIAL_MOCK_CONFIG


MOCK_CONFIG = connection_mock_config(PARTIAL_MOCK_CONFIG,
                                     base=BASE_MOCK_CONFIG,
                                     connector=('plugins', 'api', 'plugins',
                                                'contracting.core', 'plugins'))

class BaseWebTest(CoreBaseWebTest):

    relative_to = path.dirname(__file__)
    mock_config = MOCK_CONFIG
