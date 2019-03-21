Linked Data Interface
=====================

:py:mod:`qwikidata.linked_data_interface`

Description
-----------

Wikidata provides access to knowledge base entity information through a
linked data interface,

    "Each item or property has a persistent URI that you obtain by appending its ID
    (such as Q42 or P12) to the Wikidata concept namespace: http://www.wikidata.org/entity/

    For example, the concept URI of Douglas Adams is http://www.wikidata.org/entity/Q42.
    Note that this URI refers to the real-world person, not Wikidata's description of Douglas
    Adams. However, it is possible to use the concept URI to access data about Douglas Adams
    by simply using it as a URL. When you request this URL, it triggers an HTTP redirect that
    forwards the client to the data URL for Wikidata's data about Douglas Adams:
    http://www.wikidata.org/wiki/Special:EntityData/Q42. The namespace for Wikidata's data about
    entities is http://www.wikidata.org/wiki/Special:EntityData/"

    -- https://www.wikidata.org/wiki/Wikidata:Data_access


Example
-------

.. code-block:: python

  from qwikidata.linked_data_interface import get_entity_dict_from_api
  from qwikidata.entity import WikidataItem, WikidataProperty, WikidataLexeme

  q42_dict = get_entity_dict_from_api('Q42')
  q42 = WikidataItem(q42_dict)

  p279_dict = get_entity_dict_from_api('P279')
  p279 = WikidataProperty(p279_dict)

  l3_dict = get_entity_dict_from_api('L3')
  l3 = WikidataLexeme(l3_dict)
