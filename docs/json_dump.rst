JSON Dump Files
===============

:py:mod:`qwikidata.json_dump`

Description
-----------

Wikidata provides frequent (every few days) dumps of the knowledge base
in the form of compressed JSON files.  From the docs,

    "JSON dumps containing all Wikidata entities in a single JSON array can be found under
    https://dumps.wikimedia.org/wikidatawiki/entities/. The entities in the array are not
    necessarily in any particular order, e.g., Q2 doesn't necessarily follow Q1. The dumps
    are being created on a weekly basis.

    This is the recommended dump format. `Please refer to the JSON structure documentation`_
    for information about how Wikidata entities are represented.

    Hint: Each entity object (data item or property) is placed on a separate line in the JSON
    file, so the file can be read line by line, and each line can be decoded separately as an
    individual JSON object."

    -- https://www.wikidata.org/wiki/Wikidata:Database_download


Example
-------

.. code-block:: python

   from qwikidata.json_dump import WikidataJsonDump

   wjd = WikidataJsonDump('wikidata-20190107-all.json.bz2')

Iteration over the :py:class:`qwikidata.json_dump.WikidataJsonDump` object will yield dictionary
representations of entities (one entity per iteration).


.. code-block:: python

   from qwikidata.entity import WikidataItem, WikidataProperty

   type_to_entity_class = {"item": WikidataItem, "property": WikidataProperty}
   max_entities = 5
   entities = []


   for ii, entity_dict in enumerate(wjd):
     if ii >= max_entities:
       break
     entity_id = entity_dict["id"]
     entity_type = entity_dict["type"]
     entity = type_to_entity_class[entity_type](entity_dict)
     entities.append(entity)

   for entity in entities:
     print(entity)


::

    WikidataItem(label=Belgium, id=Q31, description=federal constitutional monarchy in Western Europe, aliases=['Kingdom of Belgium', 'be', '🇧🇪'], enwiki_title=Belgium)
    WikidataItem(label=happiness, id=Q8, description=mental or emotional state of well-being characterized by pleasant emotions, aliases=['😄', ':)', '😃', 'joy', 'happy'], enwiki_title=Happiness)
    WikidataItem(label=George Washington, id=Q23, description=First President of the United States, aliases=['Washington', 'President Washington', 'G. Washington', 'Father of the United States'], enwiki_title=George Washington)
    WikidataItem(label=Jack Bauer, id=Q24, description=character from the television series 24, aliases=[], enwiki_title=Jack Bauer)
    WikidataItem(label=Douglas Adams, id=Q42, description=British author and humorist (1952–2001), aliases=['Douglas Noel Adams', 'Douglas Noël Adams', 'Douglas N. Adams'], enwiki_title=Douglas Adams)


It is also possible to use the :py:func:`qwikidata.json_dump.WikidataJsonDump.create_chunks`
method to create truncated versions of the json dump file and/or break the original file into chunks,


.. code-block:: python

   # create a single chunk to get a truncated version of the file
   trunc_file_name = wjd.create_chunks(num_lines_per_chunk=5, max_chunks=1)

   # or create all the chunks
   chunk_file_names = wjd.create_chunks(num_lines_per_chunk=100_000)


.. _Please refer to the JSON structure documentation: https://www.mediawiki.org/wiki/Wikibase/DataModel/JSON
