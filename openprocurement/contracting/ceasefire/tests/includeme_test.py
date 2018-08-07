import unittest
from mock import (
    Mock,
    MagicMock,
    patch
)

from openprocurement.contracting.ceasefire.includeme import includeme


class IncludemeTest(unittest.TestCase):

    @patch('openprocurement.contracting.ceasefire.includeme.getLogger')
    @patch('openprocurement.contracting.ceasefire.includeme.get_distribution')
    def test_includeme(self, mocked_get_distribution, mocked_get_logger):
        config = MagicMock()

        plugin_config = MagicMock()
        plugin_config.get.side_effect = [[], True]
        logger = Mock()
        info = Mock()
        logger.info = info
        mocked_get_logger.return_value = logger

        includeme(config, plugin_config)

        assert info.called
        assert info.called_with('Init contracting.ceasefire plugin.')
