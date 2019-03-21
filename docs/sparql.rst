SPARQL End Point
================

:py:mod:`qwikidata.sparql`

Description
-----------

Wikidata provides endpoints to process SPARQL queries,

    SPARQL queries can be submitted directly to the SPARQL endpoint with GET request to
    `https://query.wikidata.org/bigdata/namespace/wdq/sparql?query={SPARQL}` or the endpoint's
    alias `https://query.wikidata.org/sparql?query={SPARQL}`. The result is returned as XML by
    default, or as JSON if either the query parameter format=json or the header Accept:
    application/sparql-results+json are provided. See the user manual for more detailed
    information.

    -- https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service

You can find their GUI implementation here https://query.wikidata.org/


Example
-------


We can find all items that are in the subclass tree of river.  Note that,

* ``subclass of`` is `P279 <https://www.wikidata.org/wiki/Property:P279>`_
* ``river`` is `Q4022 <https://www.wikidata.org/wiki/Q4022>`_

.. code-block:: python

  from qwikidata.sparql import return_sparql_query_results

  query_string = """
  SELECT $WDid
  WHERE {
    ?WDid (wdt:P279)* wd:Q4022
  }
  """

  results = return_sparql_query_results(query_string)


Alternatively, we can find all items that have river in their subclass tree.

.. code-block:: python

  from qwikidata.sparql import return_sparql_query_results

  query_string = """
  SELECT $WDid
  WHERE {
    wd:Q4022 (wdt:P279)* ?WDid
  }
  """

  results = return_sparql_query_results(query_string)
