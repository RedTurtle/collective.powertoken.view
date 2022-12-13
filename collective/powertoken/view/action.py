# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from zope.interface import implementer
from zope.component import getMultiAdapter

from collective.powertoken.core.interfaces import IPowerActionProvider



@implementer(IPowerActionProvider)
class ViewActionProvider(object):
    """
    Return the default view of the content
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def doAction(self, action):
        view = action.params.get('view')
        cmfcallable = action.params.get('cmfcallable')
        context = aq_inner(self.context)

        if action.params.get('setToRequest'):
            for k,v in action.params['setToRequest'].items():
                context.REQUEST.set(k, v)

        if view:
            view_to_call = getMultiAdapter((context, context.REQUEST), name=view)
            return view_to_call()

        if cmfcallable:
            return getattr(self.context, cmfcallable, self.context.view)()

        return self.context()
