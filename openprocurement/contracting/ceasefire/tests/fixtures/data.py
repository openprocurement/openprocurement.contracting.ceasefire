# -*- coding: utf-8 -*-
from openprocurement.api.utils.common import get_now

from datetime import timedelta
from copy import deepcopy


test_organization = {
    "name": u"Державне управління справами",
    "identifier": {
        "scheme": u"UA-EDR",
        "id": u"00037256",
        "uri": u"http://www.dus.gov.ua/"
    },
    "address": {
        "countryName": u"Україна",
        "postalCode": u"01220",
        "region": u"м. Київ",
        "locality": u"м. Київ",
        "streetAddress": u"вул. Банкова, 11, корпус 1"
    },
    "contactPoint": {
        "name": u"Державне управління справами",
        "telephone": u"0440000000"
    }
}
test_procuringEntity = test_organization.copy()
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
    "dateSigned": get_now().isoformat(),
    "merchandisingObject": "a930574bf8cd999cb7f9c9ed4ca68061",
    "period": {
        "startDate": get_now().isoformat(),
        "endDate": (get_now() + timedelta(days=30)).isoformat(),
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
