import unittest
from mock import (
    Mock,
    patch,
)

from openprocurement.contracting.ceasefire.includeme import includeme


class IncludemeTest(unittest.TestCase):

    @patch('openprocurement.contracting.ceasefire.includeme.getLogger')
    @patch('openprocurement.contracting.ceasefire.includeme.get_distribution')
    def test_includeme(self, mocked_get_distribution, mocked_get_logger):
        config = Mock()

        logger = Mock()
        info = Mock()
        logger.info = info
        mocked_get_logger.return_value = logger

        includeme(config)

        assert info.called
        assert info.called_with('Init contracting.ceasefire plugin.')
        assert str(config.mock_calls[0]) == \
            "call.add_contract_contractType(<class 'openprocurement.contracting.ceasefire.models.Contract'>)"
        assert str(config.mock_calls[1]) == \
            "call.scan('openprocurement.contracting.ceasefire.views')"
