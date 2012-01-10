from setuptools import setup, find_packages
import os

tests_require = ['zope.testing', 'Products.PloneTestCase']

version = '0.1.0'

setup(name='collective.powertoken.view',
      version=version,
      description="View and content access add-ons for collective.powertoken support for Plone",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 3.3",
        "Framework :: Plone :: 4.0",
        "Framework :: Plone :: 4.1",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        ],
      keywords='plone security token plonegov view access',
      author='RedTurtle Technology',
      author_email='sviluppoplone@redturtle.it',
      url='http://plone.org/collective.powertoken.core',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.powertoken'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.powertoken.core',
      ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
