from setuptools import setup, find_packages

VERSION = '1.0.5'

requires = [
    'setuptools',
]

test_requires = requires + [
    'webtest',
    'munch',
    'python-coveralls',
]

docs_requires = requires + [
    'sphinxcontrib-httpdomain',
]

api_requires = requires + [
    'openprocurement.api>=2.4',
    'openprocurement.contracting.core',
]

entry_points = {
    'openprocurement.contracting.core.plugins': [
        'contracting.ceasefire = openprocurement.contracting.ceasefire.includeme:includeme'
    ]
}

setup(name='openprocurement.contracting.ceasefire',
      version=VERSION,
      description="",
      long_description=open("README.md").read(),
      classifiers=[
          "Framework :: Pylons",
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application"
      ],
      keywords="web services",
      author='Quintagroup, Ltd.',
      author_email='info@quintagroup.com',
      license='Apache License 2.0',
      url='https://github.com/openprocurement/openprocurement.contracting.common',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['openprocurement', 'openprocurement.contracting'],
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=test_requires,
      extras_require={
          'api': api_requires,
          'test': test_requires,
          'docs': docs_requires
      },
      entry_points=entry_points,
      )
