# -*- coding: utf-8 -*-
from datetime import timedelta

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
    contract_id = create_contract(test_case, contract_data)
    response = post_document(test_case, contract_id)
    document_id = response.json['data']['id']
    return (contract_id, document_id)
