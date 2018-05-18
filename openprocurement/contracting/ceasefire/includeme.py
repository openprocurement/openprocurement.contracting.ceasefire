# -*- coding: utf-8 -*-
from logging import getLogger
from pkg_resources import get_distribution

from openprocurement.contracting.core.interfaces import (
    IContractManager,
    IMilestoneManager,
)
from openprocurement.contracting.ceasefire.adapters import (
    CeasefireContractManager,
    CeasefireMilestoneManager,
)
from openprocurement.contracting.ceasefire.models import (
    Contract,
    ICeasefireContract,
    ICeasefireMilestone,
)




def includeme(config, plugin_config=None):
    PKG = get_distribution(__package__)
    LOGGER = getLogger(PKG.project_name)

    LOGGER.info('Init contracting.ceasefire plugin.')
    config.add_contract_contractType(Contract)
    config.scan("openprocurement.contracting.ceasefire.views")
    config.registry.registerAdapter(
        CeasefireContractManager,
        (ICeasefireContract,),
        IContractManager
    )
    config.registry.registerAdapter(
        CeasefireMilestoneManager,
        (ICeasefireMilestone,),
        IMilestoneManager
    )
