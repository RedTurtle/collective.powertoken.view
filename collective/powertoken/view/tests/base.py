# -*- coding: utf-8 -*-

import unittest
from collective.powertoken.view.testing import INTEGRATION_TESTING

class TestCase(unittest.TestCase):
    """Base class used for test cases
    """

    layer = INTEGRATION_TESTING