# Copyright 2019 Kensho Technologies, LLC.
"""Module for the Wikidata SPARQL endpint."""
from typing import Dict, List, Union

import requests

WIKIDATA_SPARQL_URL = "https://query.wikidata.org/sparql"


def return_sparql_query_results(
    query_string: str, wikidata_sparql_url: str = WIKIDATA_SPARQL_URL
) -> Dict:
    """Send a SPARQL query and return the JSON formatted result.

    Parameters
    ----------
    query_string: str
      SPARQL query string
    wikidata_sparql_url: str, optional
      wikidata SPARQL endpoint to use
    """
    return requests.get(
        wikidata_sparql_url, params={"query": query_string, "format": "json"}
    ).json()


def get_subclasses_of_item(item_id: str, return_qids: bool = True) -> Union[List[str], Dict]:
    """Return all subclasses of a wikidata item.

    Finds all items where a chain of the following form exists,::

      Qid_i -[P279]-> Qid_j ... Qid_k -[P279]-> item_id

    Will always include the item itself in the return results.  Note that
    property P279 = "subclass of".

    Parameters
    ----------
    item_id: str
      The item to use as the end of the chain.
    return_qids: bool, optional
      If false, the SPARQL query result is returned unaltered.  If true,
      a list of item id string is returned instead.  See examples.

    Examples
    --------
    We can get all item IDs that are subclasses of `Q6256`,

    ::

      >>> get_subclasses_of_item('Q6256')
      ['Q6256',
       'Q112099',
       'Q123480',
       ...
       'Q4994005',
       'Q6805624',
       'Q15895923']

    ::

      >>> get_subclasses_of_item('Q6256', return_qids=False)
      {'head': {'vars': ['WDid']},
       'results': {'bindings': [
         {'WDid': {'type': 'uri',
           'value': 'http://www.wikidata.org/entity/Q6256'}},
         {'WDid': {'type': 'uri',
           'value': 'http://www.wikidata.org/entity/Q112099'}},
         ...
         {'WDid': {'type': 'uri',
           'value': 'http://www.wikidata.org/entity/Q6805624'}},
         {'WDid': {'type': 'uri',
           'value': 'http://www.wikidata.org/entity/Q15895923'}}]}}
    """
    query_string = f"""
    SELECT $WDid
    WHERE {{
      ?WDid (wdt:P279)* wd:{item_id} .
    }}
    """
    results = return_sparql_query_results(query_string)
    if return_qids:
        uris = [binding["WDid"]["value"] for binding in results["results"]["bindings"]]
        qids = [uri.split("/")[-1] for uri in uris]
        return qids
    else:
        return results
