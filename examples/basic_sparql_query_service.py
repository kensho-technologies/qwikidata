from qwikidata.sparql import (get_subclasses_of_item,
                              return_sparql_query_results)

# send any sparql query to the wikidata query service and get full result back
# here we use an example that counts the number of humans
sparql_query = """
SELECT (COUNT(?item) AS ?count)
WHERE {
        ?item wdt:P31/wdt:P279* wd:Q5 .
}
"""
res = return_sparql_query_results(sparql_query)


# use convenience function to get subclasses of an item as a list of item ids
Q_RIVER = "Q4022"
subclasses_of_river = get_subclasses_of_item(Q_RIVER)
