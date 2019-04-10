# Copyright 2019 Kensho Technologies, LLC.
"""qwikidata utilities."""

import itertools
import json
from typing import Iterable, Iterator, Tuple

from qwikidata.entity import WikidataEntity


def pairwise(iterable: Iterable) -> Iterator[Tuple]:
    """Return pairwise tuples s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def dump_entities_to_json(entities: Iterable[WikidataEntity], out_fname: str) -> None:
    """Write entities to JSON file.

    Parameters
    ----------
    entities
      An iterable of instances of WikidataEntity
    out_fname
      Output file name
    """
    with open(out_fname, "w") as fp:
        fp.write("[\n")
        for ent_lo, ent_hi in pairwise(entities):
            ent_str = json.dumps(ent_lo._entity_dict)
            fp.write("{},\n".format(ent_str))
        ent_str = json.dumps(ent_hi._entity_dict)
        fp.write("{}".format(ent_str))
        fp.write("\n]")
