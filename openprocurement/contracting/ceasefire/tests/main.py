# -*- coding: utf-8 -*-
import unittest

from openprocurement.contracting.ceasefire import (
    includeme,
)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(includeme.suite())
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
