# -*- coding: utf-8 -*-
from copy import deepcopy
from datetime import timedelta
from munch import munchify
from mock import Mock

from openprocurement.api.models.ocds import (
    BaseDocument,
)
from openprocurement.api.utils import (
    search_list_with_dicts,
)
from openprocurement.api.tests.blanks.json_data import (
    test_document_data,
)
from openprocurement.contracting.core.constants import (
    ENDPOINTS as CORE_ENDPOINTS,
)
from openprocurement.contracting.ceasefire.constants import (
    ENDPOINTS,
)
from openprocurement.contracting.ceasefire.models import (
    Contract,
    Milestone,
)
from .data import contract_create_data


def get_contract(test_case, contract_id):
    response = test_case.app.get(ENDPOINTS['contracts'].format(
        contract_id=contract_id,
        )
    )
    test_case.assertEqual(response.status, '200 OK', 'Cannot get contract')
    return Contract(response.json['data'])


def patch_contract(test_case, contract, data, status=200):
    return test_case.app.patch_json(
        ENDPOINTS['contracts'].format(
            contract_id=contract.data.id,
        ) + "?acc_token={}".format(contract.access.token),
        data,
        status=status,
    )


def get_milestone(test_case, contract_id, milestone_id):
    response = test_case.app.get(ENDPOINTS['milestones'].format(
        contract_id=contract_id,
        milestone_id=milestone_id
        )
    )
    test_case.assertEqual(response.status, '200 OK', 'Cannot get milestone')
    return Milestone(response.json['data'])


def patch_milestone(test_case, contract, milestone_id, data, status=200):
    return test_case.app.patch_json(
        ENDPOINTS['milestones'].format(
            contract_id=contract.data.id,
            milestone_id=milestone_id,
        ) + "?acc_token={}".format(contract.access.token),
        data,
        status=status,
    )


def post_document(test_case, contract, **kwargs):
    data = {}
    if not kwargs.get('data'):
        data = deepcopy(test_document_data)
        data.update({
            'url': test_case.generate_docservice_url(),
            'documentOf': 'lot',
            'relatedItem': '01' * 16
        })
    else:
        data.update(kwargs['data'])

    target_status = 201
    if kwargs.get('status_code'):
        target_status = kwargs['status_code']

    url = CORE_ENDPOINTS['documents_collection'].format(
        contract_id=contract.data.id
    ) + "?acc_token={}".format(contract.access.token)

    response = test_case.app.post_json(url, {'data': data}, status=target_status)
    return response


def put_document(test_case, contract, document_id, **kwargs):
    data = {}
    data = deepcopy(test_document_data)
    data.update({
        'url': test_case.generate_docservice_url(),
        'documentOf': 'lot',
        'relatedItem': '01' * 16
    })
    data.update(kwargs.get('data', {}))

    target_status = 200
    if kwargs.get('status_code'):
        target_status = kwargs['status_code']

    url = CORE_ENDPOINTS['documents'].format(
        contract_id=contract.data.id,
        document_id=document_id,
    ) + "?acc_token={}".format(contract.access.token)

    response = test_case.app.put_json(url, {'data': data}, status=target_status)
    return response


def get_document(test_case, contract_id, document_id, serialize=True):
    response = test_case.app.get(CORE_ENDPOINTS['documents'].format(
        contract_id=contract_id,
        document_id=document_id))
    if serialize:
        doc = BaseDocument(response.json['data'])
        doc.validate()
        return doc
    return response


def create_contract(test_case, data=None):
    if data is None:
        data = contract_create_data
    response = test_case.app.post_json(
        ENDPOINTS['contracts_collection'],
        {
            'data': data,
        }
    )
    assert response.status == '201 Created', 'Contract not created'
    return munchify(response.json)


def post_milestone_document(test_case, contract, milestone_id, **kwargs):
    doc_data = deepcopy(test_document_data)
    doc_data.update({
        'url': test_case.generate_docservice_url(),
        'documentOf': 'milestone',
        'relatedItem': milestone_id
    })
    doc_data.update(kwargs)
    return post_document(test_case, contract, data=doc_data)


def patch_milestone_document(test_case, contract, milestone_id, document_id, data):
    return test_case.app.patch_json(
        CORE_ENDPOINTS['documents'].format(
            contract_id=contract.data.id,
            milestone_id=milestone_id,
            document_id=document_id,
        ) + "?acc_token={}".format(contract.access.token),
        data,
        status=200
    )


def prepare_milestones(test_case, contract_data=None, doc_preload=True):
    """Prepares contract's milestones to make financing milestone have processing status
    """
    contract = create_contract(test_case, contract_data)
    # milestones will be populated when status changes to 'active.payment'
    contract_patch_response = patch_contract(
        test_case,
        contract,
        {'data': {'status': 'active.payment'}},
    )
    test_case.assertEqual(contract_patch_response.status, '200 OK')
    milestones = munchify(contract_patch_response.json['data']['milestones'])
    if doc_preload:
        for milestone in milestones:
            post_milestone_document(test_case, contract, milestone.id)
    return (contract, milestones)


def prepare_milestones_approval(test_case, contract_data=None):
    """Prepares contract's milestones to make financing milestone have processing status
    """
    contract, milestones = prepare_milestones(test_case, contract_data)
    financing_milestone = Milestone(milestones[0])
    assert financing_milestone.type_ == 'financing'
    dateMet_to_set = financing_milestone.dueDate - timedelta(days=5)

    response = patch_milestone(
        test_case,
        contract,
        financing_milestone.id,
        {'data': {'dateMet': dateMet_to_set.isoformat()}}
    )
    test_case.assertEqual(response.status, '200 OK')
    resp = get_contract(test_case, contract.data.id)
    contract.data.update(resp)
    return (contract, contract.data.milestones)


def prepare_milestones_reporting(test_case, contract_data=None):
    """Prepares contract's milestones to make approval milestone have processing status
    """
    contract, milestones = prepare_milestones_approval(test_case, contract_data)
    approval_milestone = milestones[1]
    assert approval_milestone.type_ == 'approval'
    dateMet_to_set = approval_milestone.dueDate - timedelta(days=5)

    response = patch_milestone(
        test_case,
        contract,
        approval_milestone.id,
        {'data': {'dateMet': dateMet_to_set.isoformat()}}
    )
    test_case.assertEqual(response.status, '200 OK')
    resp = get_contract(test_case, contract.data.id)
    contract.data.update(resp)
    return (contract, contract.data.milestones)


def prepare_milestones_all_met(test_case, contract_data=None):
    contract, milestones = prepare_milestones_reporting(test_case, contract_data)
    reporting_milestone = search_list_with_dicts(milestones, 'type_', 'reporting')
    dateMet_to_set = reporting_milestone.dueDate - timedelta(days=5)

    assert reporting_milestone.type_ == 'reporting'

    response = patch_milestone(
        test_case,
        contract,
        reporting_milestone.id,
        {'data': {'dateMet': dateMet_to_set.isoformat()}}
    )

    test_case.assertEqual(response.status, '200 OK')
    resp = get_contract(test_case, contract.data.id)
    contract.data.update(resp)
    return (contract, contract.data.milestones)


def prepare_contract_with_document(test_case, contract_data=None):
    contract = create_contract(test_case, contract_data)
    response = post_document(test_case, contract)
    document = munchify(response.json)
    return (contract, document)


def prepare_contract():
    contract = Contract(contract_create_data)
    contract.validate()

    return contract

def prepare_contract_with_milestones():
    from openprocurement.contracting.ceasefire.adapters.milestone_manager import CeasefireMilestoneManager

    contract = prepare_contract()
    milestone_manager = CeasefireMilestoneManager()
    milestone_manager.create_milestones(contract)

    return contract
