# Copyright 2019 Kensho Technologies, LLC.
"""qwikidata utilities."""

import itertools
from typing import Iterable, Iterator, Tuple


def pairwise(iterable: Iterable) -> Iterator[Tuple]:
    """Return pairwise tuples s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)
