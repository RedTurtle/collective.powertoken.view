# -*- coding: utf-8 -*-
import os 

from AccessControl import Unauthorized
from zope.component import getUtility, getMultiAdapter

from plone.app.testing import setRoles, TEST_USER_ID
from plone.app.testing import logout

from collective.powertoken.core.interfaces import IPowerTokenUtility

from collective.powertoken.view import tests
from collective.powertoken.view.tests.base import TestCase

from plone.app.textfield.value import RichTextValue


class TestViewAction(TestCase):

    def setUp(self):
        """ """
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory(type_name="Document", id="testdoc")
        doc = self.portal.testdoc
        doc.title = "A test document"
        doc.text = RichTextValue(
                      "<p>This is the secret password: The Cat Is On The Table</p>", 
                      'text/html', 
                      'text/html')
        self.doc = doc
        self.utility = getUtility(IPowerTokenUtility)
        self.request = self.portal.REQUEST


    def test_actionSimpleView(self):
        """ """
        token = self.utility.enablePowerToken(self.doc, 'view.viewDocument')
        output = self.utility.consumeActions(self.doc, token)[0]
        self.assertTrue('This is the secret password: The Cat Is On The Table' in output)

        # this is not working
        #logout()
        #token = self.utility.enablePowerToken(self.doc, 'view.viewDocument')
        #output = self.utility.consumeActions(self.doc, token)[0]
        #self.assertRaises(Unauthorized, self.utility.consumeActions, self.doc, token)

        token = self.utility.enablePowerToken(self.doc, 'view.viewDocument', roles=['Reader'])
        output = self.utility.consumeActions(self.doc, token)[0]
        self.assertTrue('This is the secret password: The Cat Is On The Table' in output)


    def test_actionZopeView(self):
        """ """
        # to check simple_view render:
        # from zope.component import getMultiAdapter
        # view = getMultiAdapter((self.doc, self.request), name='simple_view')

        token = self.utility.enablePowerToken(
                                self.doc, 
                                'view.viewDocument', 
                                view='simple_view')
        output = self.utility.consumeActions(self.doc, token)[0]
        self.assertTrue('A test document' in output)

        logout()
        token = self.utility.enablePowerToken(
                                self.doc, 
                                'view.viewDocument', 
                                roles=['Owner'], 
                                view='simple_view')
        output = self.utility.consumeActions(self.doc, token)[0]
        self.assertTrue('A test document' in output)


    def test_actionCMFCallable(self):
        """ """
        # simple_view should be registered as template in a skin
        view = getMultiAdapter((self.doc, self.request), name='simple_view')
        setattr(self.doc, 'simple_view', view)

        token = self.utility.enablePowerToken(
                                self.doc, 
                                'view.viewDocument', 
                                cmfcallable='simple_view')
        output = self.utility.consumeActions(self.doc, token)[0]
        self.assertTrue('A test document' in output)

        logout()
        token = self.utility.enablePowerToken(
                                self.doc, 
                                'view.viewDocument', 
                                roles=['Reader'], 
                                cmfcallable='simple_view')
        output = self.utility.consumeActions(self.doc, token)[0]
        self.assertTrue('A test document' in output)
        self.assertTrue('This is the secret password: The Cat Is On The Table' in output)


    def test_setToRequest(self):
        """ verify that setToRequest is inserted in request """ 
        logout()
        token = self.utility.enablePowerToken(self.doc, 'view.viewDocument',
                                              roles=['Owner'],
                                              view='simple_view',
                                              setToRequest={'user': TEST_USER_ID})
        output = self.utility.consumeActions(self.doc, token)[0]
        self.assertTrue('user=test_user_1_' in output)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestViewAction))
    return suite
