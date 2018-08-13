# -*- coding: utf-8 -*-
from copy import deepcopy

from openprocurement.api.models.ocds import (
    BaseDocument,
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


def get_document(test_case, contract_id, document_id, serialize=True):
    response = test_case.app.get(CORE_ENDPOINTS['documents'].format(
        contract_id=contract_id,
        document_id=document_id))
    if serialize:
        doc = BaseDocument(response.json['data'])
        doc.validate()
        return doc
    return response


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
