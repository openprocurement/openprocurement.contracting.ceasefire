# -*- coding: utf-8 -*-
from datetime import datetime

from openprocurement.api.utils import (
    APIResource,
    context_unpack,
    json_view,
)
from openprocurement.contracting.core.utils import (
    apply_patch,
    contractingresource,
)
from openprocurement.contracting.core.interfaces import (
    IMilestoneManager,
)
from openprocurement.contracting.ceasefire.constants import (
    ENDPOINTS,
)
from openprocurement.contracting.ceasefire.validators import (
    validate_patch_milestone_data,
)


@contractingresource(
    name='Ceasefire Milestone',
    path=ENDPOINTS['milestones'],
    collection_path=ENDPOINTS['milestones_collection'])
class CeasefireMilestoneResource(APIResource):

    @json_view(
        permission='view_contract',
        content_type='application/json')
    def get(self):
        return {'data': self.request.context.serialize()}

    @json_view(
        permission='edit_contract',
        content_type='application/json',
        validators=(validate_patch_milestone_data,))
    def patch(self):
        manager = self.request.registry.getAdapter(self.request.context, IMilestoneManager)
        manager.change_milestone(self.request)
        self.request.context.dateModified = datetime.now()
        if apply_patch(self.request):
            self.LOGGER.info(
                'Updated ceasefire milestone {}'.format(
                    self.request.context.id
                ),
                extra=context_unpack(
                    self.request,
                    {'MESSAGE_ID': 'ceasefire_milestone_patch'}
                    )
                )
            return {'data': self.request.context.serialize()}
