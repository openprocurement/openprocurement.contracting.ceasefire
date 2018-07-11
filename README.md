# Ceasefire contracting

![CodeFactor](https://www.codefactor.io/repository/github/openprocurement/openprocurement.contracting.ceasefire/badge)

## Documentation

The documentation of this project may be built with Sphinx.

### How to build it

Commands to build the docs:

`python bootstrap.py -c docs.cfg --buildout-version 2.2.5`

`./bin/buildout -c docs.cfg`

`./bin/docs`

To set language or manage some other stuff, edit `docs/source/conf.py`

To update files with requests data for tutorial:

`./bin/buildout` to restore `nosetests` in the `bin` directory

`./bin/nosetests -sv docs/update_tutorial_requests.py`

There is deeper doc about building docs, but it can be obsolete somewhere:
[Docs instruction](https://tinyurl.com/yahvn2p7)
