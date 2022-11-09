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
        fp.write("[")
        ent_iter = iter(entities)
        ent = next(ent_iter, None)
        while ent:
            ent_str = json.dumps(ent._entity_dict)
            fp.write("\n{}".format(ent_str))
            ent = next(ent_iter, None)
            if ent: fp.write(",")

        fp.write("\n]")
