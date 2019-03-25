=======
Welcome
=======

|build-status|
|docs|
|license|
|pypi-python|
|pypi-version|


`qwikidata` is a Python package with tools that allow you to interact with Wikidata_.

The package defines a set of classes that allow you to represent Wikidata entities
in a Pythonic way.  It also provides a Pythonic way to access three data sources,

* `linked data interface`_
* `sparql query service`_
* `json dump`_

Important Links
===============

* documentation: https://qwikidata.rtfd.io/
* PyPI: https://pypi.org/project/qwikidata/
* github: https://github.com/kensho-technologies/qwikidata/

Quick Install
=============

Requirements
------------

* python >= 3.6

Install with pip
----------------

You can install the most recent version using pip,

.. code-block:: bash

  pip install qwikidata


Quick Start
===========

.. code-block:: python

  from qwikidata.linked_data_interface import get_entity_dict_from_api
  from qwikidata.entity import WikidataItem, WikidataProperty, WikidataLexeme

  q42_dict = get_entity_dict_from_api('Q42')
  q42 = WikidataItem(q42_dict)

  p279_dict = get_entity_dict_from_api('P279')
  p279 = WikidataProperty(p279_dict)

  l3_dict = get_entity_dict_from_api('L3')
  l3 = WikidataLexeme(l3_dict)


License
=======

Licensed under the Apache 2.0 License. Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

Copyright
=========

Copyright 2019 Kensho Technologies, LLC.


.. |build-status| image:: https://img.shields.io/travis/kensho-technologies/qwikidata.svg?style=flat
    :alt: Build Status
    :scale: 100%
    :target: https://travis-ci.org/kensho-technologies/qwikidata

.. |docs| image:: https://readthedocs.org/projects/qwikidata/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://qwikidata.readthedocs.io/en/latest/?badge=latest

.. |license| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
    :alt: License
    :scale: 100%
    :target: https://opensource.org/licenses/Apache-2.0

.. |pypi-python| image:: https://img.shields.io/pypi/pyversions/qwikidata.svg
    :alt: PyPI Python
    :scale: 100%
    :target: https://pypi.python.org/pypi/qwikidata

.. |pypi-version| image:: https://img.shields.io/pypi/v/qwikidata.svg
   :alt: PyPI Version
   :scale: 100%
   :target: https://pypi.python.org/pypi/qwikidata


.. _Wikidata: https://www.wikidata.org/wiki/Wikidata:Main_Page
.. _linked data interface: https://www.wikidata.org/wiki/Wikidata:Data_access
.. _sparql query service: https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service
.. _json dump: https://www.wikidata.org/wiki/Wikidata:Database_download
