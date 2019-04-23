# -*- coding: utf-8 -*-
from openprocurement.api.utils import (
    APIResource,
    json_view,
)
from openprocurement.api.utils.error_management import handle_errors_on_view
from openprocurement.contracting.core.utils import (
    contractingresource,
)
from openprocurement.contracting.ceasefire.constants import (
    CONTRACT_DEFAULT_TYPE,
    ENDPOINTS,
)
from openprocurement.api.validation import validate_data_to_event
from openprocurement.contracting.core.manager_discovery import ContractManagerDiscovery


@contractingresource(
    name='ceasefire:Contract',
    path=ENDPOINTS['contracts'],
    collection_path=ENDPOINTS['contracts_collection'],
    internal_type=CONTRACT_DEFAULT_TYPE)
class CeasefireContractResource(APIResource):

    @json_view(permission='view_contract')
    def get(self):
        return {'data': self.request.context.serialize("view")}

    @handle_errors_on_view
    @json_view(
        permission='edit_contract',
        validators=(validate_data_to_event,)
    )
    def patch(self):
        event = self.request.event
        md = ContractManagerDiscovery(self.request.registry.manager_registry)
        manager = md.discover(event.ctx.high)()
        return manager.change_contract(event)
