# -*- coding: utf-8 -*-
from openprocurement.contracting.ceasefire.constants import (
    ENDPOINTS,
)
from .data import contract_create_data


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
    return response.json['data']['id']
