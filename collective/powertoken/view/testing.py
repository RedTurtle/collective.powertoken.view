# -*- coding: utf-8 -*-
import os

from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import (
    IntegrationTesting,
    PloneSandboxLayer,
)


from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from zope.publisher.interfaces.browser import IBrowserPage
from zope.publisher.browser import BrowserPage
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.component import adapter, provideAdapter
from zope.interface import Interface
from zope.publisher.interfaces.browser import IHTTPRequest
from Products.CMFCore.interfaces import IContentish

from collective.powertoken.view import tests


@adapter(Interface, IBrowserRequest)
class SimpleView(BrowserPage):

    __call__ = ViewPageTemplateFile(
                  'simple_view.pt', os.path.dirname(tests.__file__))


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import collective.powertoken.core
        import collective.powertoken.view
        self.loadZCML(package=collective.powertoken.core)
        self.loadZCML(package=collective.powertoken.view)

        provideAdapter(
            SimpleView, 
            (IContentish, IHTTPRequest),
            provides=IBrowserPage, 
            name='simple_view')

FIXTURE = Fixture()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='CollectivePowertokenViewLayer:Integration',
)
