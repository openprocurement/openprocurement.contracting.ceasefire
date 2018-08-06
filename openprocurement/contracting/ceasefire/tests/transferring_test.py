# -*- coding: utf-8 -*-
import unittest

from openprocurement.contracting.ceasefire.tests.base import BaseContractWebTest
from openprocurement.contracting.core.tests.plugins.transferring.mixins import (
    ContractOwnershipChangeTestCaseMixin
)


class ContractOwnershipChangeResourceTest(BaseContractWebTest, ContractOwnershipChangeTestCaseMixin):

    def setUp(self):
        super(ContractOwnershipChangeResourceTest, self).setUp()
        self.not_used_transfer = self.create_transfer()


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(ContractOwnershipChangeResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
