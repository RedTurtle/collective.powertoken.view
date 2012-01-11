Introduction
============

A "view document" action implementation for `collective.powertoken`__

__ http://plone.org/products/collective.powertoken.core

How to use
==========

Add this product to your Plone installation, then you will be able to register Power Tokens that
"view" document.

>>> from collective.powertoken.core.interfaces import IPowerTokenUtility
>>> utility = getUtility(IPowerTokenUtility)
>>> token = utility.enablePowerToken(document, 'view.viewDocument')
>>> results = utility.consumeAction(document, token)
>>> print results
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" ...
...
</html>

You will get the view output as result.

Parameters
----------

``view``
    Call a different Zope view on the context, not the current or default ones.
``cmfcallable``
    Call a CMF Template/skins resource on the context
``setToRequest``
    A dict with additional values to set in the request. For example you can set ``disable_border``, or
    (only for Plone 4) ``disable_plone.leftcolumn`` and ``disable_plone.rightcolumn``.

Both parameter are not mandatory. Providing none of theme will call the content default view.

Use case
========

* You can view a document, regardless of it's review state and your roles in the site.
* You can call a view on a context, overriding the user security permission.

Authors
=======

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.it/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.it/
