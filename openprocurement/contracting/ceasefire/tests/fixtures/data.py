# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from copy import deepcopy

from openprocurement.auctions.core.tests.base import (
    test_organization,
    test_procuringEntity,
)


swiftsure_procuring_entity = deepcopy(test_procuringEntity)
swiftsure_procuring_entity.update({
    "additionalContactPoints": [
        {
            "name": u"Державне управління справами",
            "telephone": u"0440000000"
        }
    ]
})

contract_create_data = {
    "awardID": "376d560b2b2d452a80543865f3cab43e",
    "contractID": "a930574bf8cd405cb7f9c9ed4ca68061",
    "contractType": "ceasefire",
    "dateSigned": datetime.now().isoformat(),
    "merchandisingObject": "a930574bf8cd999cb7f9c9ed4ca68061",
    "period": {
        "startDate": datetime.now().isoformat(),
        "endDate": (datetime.now() + timedelta(days=30)).isoformat(),
    },
    "procuringEntity": swiftsure_procuring_entity,
    "title": "Test Contract",
    "suppliers": [test_organization],
    "value": {
     "currency": "UAH",
     "amount": 500.0,
     "valueAddedTaxIncluded": True
    },
    "items": [
        {
            "description": u"Земля для військовослужбовців",
            "classification": {
                "scheme": u"CPV",
                "id": u"66113000-5",
                "description": u"Земельні ділянки"
            },
            "unit": {
                "name": u"item",
                "code": u"44617100-9"
            },
            "quantity": 5,
            "registrationDetails": {
                "status": "unknown",
            },
            "address": {
                "countryName": u"Україна",
                "postalCode": "79000",
                "region": u"м. Київ",
                "locality": u"м. Київ",
                "streetAddress": u"вул. Банкова 1"
            }
        }
    ]
}
