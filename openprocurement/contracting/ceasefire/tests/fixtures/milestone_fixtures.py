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
)
from openprocurement.contracting.ceasefire.models import (
    Milestone,
)


def prepare_milestones(test_case, contract_data=None):
    """Prepares contract's milestones to make financing milestone have processing status
    """
    contract_id = create_contract(test_case, contract_data)
    patch_contract_url = ENDPOINTS['contracts'].format(contract_id=contract_id)
    # milestones will be populated when status changes to 'active.payment'
    contract_patch_response = test_case.app.patch_json(
        patch_contract_url,
        {'data': {'status': 'active.payment'}}
    )
    test_case.assertEqual(contract_patch_response.status, '200 OK')
    milestones = contract_patch_response.json['data']['milestones']
    return (contract_id, milestones)


def prepare_milestones_approval(test_case, contract_data=None):
    """Prepares contract's milestones to make financing milestone have processing status
    """
    contract_id, milestones = prepare_milestones(test_case, contract_data)
    financing_milestone = Milestone(milestones[0])
    assert financing_milestone.type_ == 'financing'
    dateMet_to_set = financing_milestone.dueDate - timedelta(days=5)

    response = test_case.app.patch_json(
        ENDPOINTS['milestones'].format(
            contract_id=contract_id,
            milestone_id=milestones[0]['id'],
        ),
        {'data': {'dateMet': dateMet_to_set.isoformat()}}
    )
    test_case.assertEqual(response.status, '200 OK')
    contract = get_contract(test_case, contract_id)
    return (contract_id, contract.milestones)


def prepare_milestones_reporting(test_case, contract_data=None):
    """Prepares contract's milestones to make approval milestone have processing status
    """
    contract_id, milestones = prepare_milestones_approval(test_case, contract_data)
    approval_milestone = milestones[1]
    assert approval_milestone.type_ == 'approval'
    dateMet_to_set = approval_milestone.dueDate - timedelta(days=5)

    response = test_case.app.patch_json(
        ENDPOINTS['milestones'].format(
            contract_id=contract_id,
            milestone_id=approval_milestone['id'],
        ),
        {'data': {'dateMet': dateMet_to_set.isoformat()}}
    )
    test_case.assertEqual(response.status, '200 OK')
    contract = get_contract(test_case, contract_id)
    return (contract_id, contract.milestones)
