# -*- coding: utf-8 -*-
from datetime import timedelta
from munch import munchify

from openprocurement.contracting.ceasefire.tests.fixtures.contract_fixtures import (
    create_contract,
)
from openprocurement.contracting.ceasefire.constants import (
    ENDPOINTS,
)
from openprocurement.contracting.ceasefire.tests.helpers import (
    get_contract,
    post_document,
)
from openprocurement.contracting.ceasefire.models import (
    Milestone,
)


def prepare_contract_with_document(test_case, contract_data=None):
    contract = create_contract(test_case, contract_data)
    response = post_document(test_case, contract)
    document = munchify(response.json)
    return (contract, document)
