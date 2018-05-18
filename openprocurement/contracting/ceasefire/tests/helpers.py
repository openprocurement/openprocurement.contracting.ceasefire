# -*- coding: utf-8 -*-
from openprocurement.contracting.ceasefire.constants import (
    ENDPOINTS,
)
from openprocurement.contracting.ceasefire.models import (
    Contract,
    Milestone,
)


def get_contract(test_case, contract_id):
    response = test_case.app.get(ENDPOINTS['contracts'].format(
        contract_id=contract_id,
        )
    )
    test_case.assertEqual(response.status, '200 OK', 'Cannot get contract')
    return Contract(response.json['data'])


def get_milestone(test_case, contract_id, milestone_id):
    response = test_case.app.get(ENDPOINTS['milestones'].format(
        contract_id=contract_id,
        milestone_id=milestone_id
        )
    )
    test_case.assertEqual(response.status, '200 OK', 'Cannot get milestone')
    return Milestone(response.json['data'])


def patch_milestone(test_case, contract_id, milestone_id, data, status=200):
    return test_case.app.patch_json(
        ENDPOINTS['milestones'].format(
            contract_id=contract_id,
            milestone_id=milestone_id,
        ),
        data,
        status=status,
    )
