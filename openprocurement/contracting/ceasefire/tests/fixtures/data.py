# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from openprocurement.auctions.core.tests.base import (
    test_organization,
    test_procuringEntity,
)


contract_create_data = {
    'awardID': '376d560b2b2d452a80543865f3cab43e',
    'contractID': 'a930574bf8cd405cb7f9c9ed4ca68061',
    'contractType': 'ceasefire',
    'dateSigned': datetime.now().isoformat(),
    'period': {
        'startDate': datetime.now().isoformat(),
        'endDate': (datetime.now() + timedelta(days=30)).isoformat(),
    },
    'auction_token': '21c5ba429b1a434ea1bfa5f70a0f5885',
    'auction_id': '0b7bca6feeb644e987ded0429f1ec167',
    'procuringEntity': test_procuringEntity,
    'title': 'Test Contract',
    'suppliers': [test_organization],
}
