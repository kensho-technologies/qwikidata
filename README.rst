=======
Welcome
=======

`qwikidata` is a Python package with tools that allow you to interact with Wikidata_.

The package defines a set of classes that allow you to represent Wikidata entities
in a Pythonic way.  It also provides a Pythonic way to access three data sources,

* `linked data interface`_
* `sparql query service`_
* `json dump`_

Full Documentation
==================

The full documentation for this project is hosted at https://qwikidata.readthedocs.io/en/latest/

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

Copyright 2019 Kensho Technologies, Inc.



.. _Wikidata: https://www.wikidata.org/wiki/Wikidata:Main_Page
.. _linked data interface: https://www.wikidata.org/wiki/Wikidata:Data_access
.. _sparql query service: https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service
.. _json dump: https://www.wikidata.org/wiki/Wikidata:Database_download
