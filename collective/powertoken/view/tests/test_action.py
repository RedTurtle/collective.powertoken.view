# -*- coding: utf-8 -*-

from zope.component import getUtility
from zope.annotation.interfaces import IAnnotations

from zope.component import provideAdapter
from zope.component import getGlobalSiteManager

from zope.publisher.interfaces.browser import IHTTPRequest

from AccessControl import Unauthorized
from Products.CMFCore.interfaces import IContentish

from collective.powertoken.core.interfaces import IPowerTokenUtility
from collective.powertoken.core.exceptions import PowerTokenConfigurationError

from collective.powertoken.view.tests.base import TestCase

class TestView(TestCase):

    def afterSetUp(self):
        self.setRoles(('Manager', ))
        portal = self.portal
        portal.invokeFactory(type_name="Document", id="testdoc")
        doc = portal.testdoc
        doc.edit(title="A test document", text="<p>This is the secret password: The Cat Is On The Table</p>")
        self.doc = doc
        self.utility = getUtility(IPowerTokenUtility)
        self.request = self.portal.REQUEST

    def test_actionSimpleView(self):
        token = self.utility.enablePowerToken(self.doc, 'view.viewDocument')
        output = self.utility.consumeActions(self.doc, token)[0]
        self.assertTrue('This is the secret password: The Cat Is On The Table' in output)
        self.logout()
        self.setRoles(('Anonymous', ))
        token = self.utility.enablePowerToken(self.doc, 'view.viewDocument')
        self.assertRaises(Unauthorized, self.utility.consumeActions, self.doc, token)
        token = self.utility.enablePowerToken(self.doc, 'view.viewDocument', roles=['Reader'])
        output = self.utility.consumeActions(self.doc, token)[0]
        self.assertTrue('This is the secret password: The Cat Is On The Table' in output)

    def test_actionZopeView(self):
        token = self.utility.enablePowerToken(self.doc, 'view.viewDocument', view='sharing')
        output = self.utility.consumeActions(self.doc, token)[0]
        self.assertTrue('user-group-sharing-head' in output)
        self.logout()
        self.setRoles(('Anonymous', ))
        token = self.utility.enablePowerToken(self.doc, 'view.viewDocument', roles=['Owner'], view='sharing')
        output = self.utility.consumeActions(self.doc, token)[0]
        self.assertTrue('user-group-sharing-head' in output)

    def test_actionCMFCallable(self):
        token = self.utility.enablePowerToken(self.doc, 'view.viewDocument', cmfcallable='base_view')
        output = self.utility.consumeActions(self.doc, token)[0]
        self.assertTrue('This is the secret password: The Cat Is On The Table' in output)
        self.logout()
        self.setRoles(('Anonymous', ))
        token = self.utility.enablePowerToken(self.doc, 'view.viewDocument', roles=['Reader'], cmfcallable='base_view')
        output = self.utility.consumeActions(self.doc, token)[0]
        self.assertTrue('This is the secret password: The Cat Is On The Table' in output)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestView))
    return suite
