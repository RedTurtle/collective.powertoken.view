# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from zope.interface import implements
from zope.component import getMultiAdapter

from collective.powertoken.core.interfaces import IPowerActionProvider

class ViewActionProvider(object):
    """
    Return the default view of the content
    """

    implements(IPowerActionProvider)
    
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
            view_to_call = view_to_call.__of__(context)
            return view_to_call()
        if cmfcallable:
            return self.context.base_view()
        return self.context()
