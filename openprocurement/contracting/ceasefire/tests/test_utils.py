# -*- coding: utf-8 -*-
import unittest

from openprocurement.contracting.ceasefire.utils import search_list_with_dicts


class TestSearchListWithDicts(unittest.TestCase):

    def setUp(self):
        self.container = (
            {
                'login': 'user1',
                'password': 'qwerty123',
            },
            {
                'login': 'user2',
                'password': 'abcd321',
                'other': 'I am User',
            }
        )

    def test_successful_search(self):
        result = search_list_with_dicts(self.container, 'login', 'user2')
        assert result['other'] == 'I am User'

    def test_unsuccessful_search(self):
        result = search_list_with_dicts(self.container, 'login', 'user3')
        assert result is None
