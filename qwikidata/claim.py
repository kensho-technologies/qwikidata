# Copyright 2019 Kensho Technologies, LLC.
"""Module for Wikidata Claims (aka Statements)."""

from collections import OrderedDict
from collections.abc import Sequence
from typing import List, Union, overload

from qwikidata import types as types
from qwikidata.snak import WikidataSnak


class WikidataReference:
    """A reference about a claim about a Wikidata Entity.

    See: https://www.wikidata.org/wiki/Help:Sources

    This class can be initialized from an entity dictionary as,

    .. code-block:: python

      >>> reference_dict = q42_dict['claims']['P69'][0]['references'][0]
      >>> wikidata_reference = WikidataReference(reference_dict)


    Parameters
    ----------
    reference_dict
      A dictionary representing a Wikidata reference.
      See `the wikibase JSON data model docs`_ for a description
      of the format.


    Attributes
    ----------
    referencehash: str
      Unique id for this reference
    snaks: collections.OrderedDict
      Maps property id to list of :py:class:`.WikidataSnak`
    """

    def __init__(self, reference_dict: types.ReferenceDict) -> None:
        self._validate_reference_dict(reference_dict)
        self._reference_dict = reference_dict

        self.referencehash = reference_dict["hash"]
        self.snaks: OrderedDict = OrderedDict()
        for property_id in reference_dict["snaks-order"]:
            self.snaks[property_id] = [
                WikidataSnak(snak_dict) for snak_dict in reference_dict["snaks"][property_id]
            ]

    def _validate_reference_dict(self, reference_dict: types.ReferenceDict) -> None:
        """Raise excpetions if reference_dict is not valid."""
        _REQUIRED_KEYS = ["hash", "snaks", "snaks-order"]
        for req_key in _REQUIRED_KEYS:
            if req_key not in reference_dict:
                raise ValueError(
                    f"required reference_dict keys are {_REQUIRED_KEYS}. "
                    f"only found {list(reference_dict.keys())}"
                )

    def __str__(self) -> str:
        return f"WikidataReference(hash={self.referencehash}, snaks={self.snaks})"

    def __repr__(self) -> str:
        return self.__str__()


class WikidataQualifier:
    """A qualifier about a claim about a Wikidata Entity.

    See: https://www.wikidata.org/wiki/Help:Qualifiers

    This class can be initialized from an entity dictionary as,

    .. code-block:: python

      >>> qualifier_dict = q42_dict['claims']['P69'][0]['qualifiers']['P582'][0]
      >>> wikidata_qualifier = WikidataQualifier(qualifier_dict)


    Parameters
    ----------
    qualifier_dict
      A dictionary representing a Wikidata qualifier.
      See `the wikibase JSON data model docs`_ for a description
      of the format.


    Attributes
    ----------
    qualifierhash: str
      Unique id for this qualifier
    snak: WikidataSnak
      The snak for this qualifier

    """

    def __init__(self, qualifier_dict: types.QualifierDict) -> None:
        self._validate_qualifier_dict(qualifier_dict)
        self._qualifier_dict = qualifier_dict

        self.qualifierhash = qualifier_dict["hash"]
        self.snak = WikidataSnak(qualifier_dict)

    def _validate_qualifier_dict(self, qualifier_dict: types.QualifierDict) -> None:
        """Raise excpetions if qualifier_dict is not valid."""
        _REQUIRED_KEYS = ["hash", "snaktype", "property", "datavalue", "datatype"]
        for req_key in _REQUIRED_KEYS:
            if req_key not in qualifier_dict:
                raise ValueError(
                    f"required qualifier_dict keys are {_REQUIRED_KEYS}. "
                    f"only found {list(qualifier_dict.keys())}"
                )

    def __str__(self) -> str:
        return f"WikidataQualifier(hash={self.qualifierhash}, snak={self.snak})"

    def __repr__(self) -> str:
        return self.__str__()


class WikidataClaim:
    """A claim aka statement about a Wikidata Entity.

    From the Wikibase data model docs,

        "Statements describe the claim of a statement and list references for this claim.
        Every Statement refers to one particular Entity, called the subject of the Statement.
        There is always one main Snak that forms the most important part of the statement.
        Moreover, there can be zero or more additional PropertySnaks that describe the Statement
        in more detail. These qualifier Snaks (or "qualifiers" for short) store additional
        information that does not directly refer to the subject (e.g., the time at which the
        main part of the statement was valid). References are provided as a list (the order is
        significant in some contexts, especially for displaying a main reference)."

        -- https://www.mediawiki.org/wiki/Wikibase/DataModel


    This class can be initialized from an entity dictionary as,

    .. code-block:: python

      >>> claim_dict = q42_dict['claims']['P551'][0]
      >>> wikidata_claim = WikidataClaim(claim_dict)


    Parameters
    ----------
    claim_dict: dict
      A dictionary representing a Wikidata claim.
      See `the wikibase JSON data model docs`_ for a description
      of the format.


    Attributes
    ----------
    claim_id: str
      Unique id for this claim
    property_id: PropertyId
      A Wikiata property id (e.g. "P551")
    claim_type: str
      One of ["claim", "statement"] (statements may have references)
    rank: str
      One of ["preferred", "normal", "deprecated"]
    mainsnak: :py:class:`.WikidataSnak`
      The mainsnak of this claim
    qualifiers: collections.OrderedDict
      Maps property id to list of :py:class:`WikidataQualifier`
    references: list
      A list of :py:class:`WikidataReference`
    qualifiers_order: list
      The order of the property ids in qualifiers


    .. _the wikibase JSON data model docs: https://www.mediawiki.org/wiki/Wikibase/DataModel/JSON
    """

    def __init__(self, claim_dict: types.ClaimDict) -> None:
        self._validate_claim_dict(claim_dict)
        self._claim_dict = claim_dict
        self.property_id = self.mainsnak.property_id

        self.qualifiers: OrderedDict[types.PropertyId, List[WikidataQualifier]] = OrderedDict()
        self.qualifiers_order = claim_dict.get("qualifiers-order", [])
        if "qualifiers" in claim_dict:
            for property_id in self.qualifiers_order:
                qualifier_dicts = claim_dict["qualifiers"][property_id]
                self.qualifiers[property_id] = [WikidataQualifier(qd) for qd in qualifier_dicts]

        self.references: List[WikidataReference] = []
        if "references" in claim_dict:
            for reference_dict in claim_dict["references"]:
                self.references.append(WikidataReference(reference_dict))

    def _validate_claim_dict(self, claim_dict: types.ClaimDict) -> None:
        """Raise excpetions if claim_dict is not valid."""
        _REQUIRED_KEYS = ["id", "type", "rank", "mainsnak"]
        for req_key in _REQUIRED_KEYS:
            if req_key not in claim_dict:
                raise ValueError(
                    f"required claim_dict keys are {_REQUIRED_KEYS}. "
                    f"only found {list(claim_dict.keys())}"
                )
        self.claim_id = claim_dict["id"]
        self.claim_type = claim_dict["type"]
        self.rank = claim_dict["rank"]
        self.mainsnak = WikidataSnak(claim_dict["mainsnak"])

    def __str__(self) -> str:
        return f"WikidataClaim(type={self.claim_type}, rank={self.rank}, mainsnak={self.mainsnak}, qualifiers={self.qualifiers})"

    def __repr__(self) -> str:
        return self.__str__()


class WikidataClaimGroup(Sequence):
    """A sequence of :py:class:`WikidataClaim` instances with a common property id.

    For example the claim group for "Douglas Adams" (Q42) with property "residence" (P551)
    has three elements.  This class can be initialized from an entity dictionary as,

    .. code-block:: python

      >>> claim_group = WikidataClaimGroup(q42_dict['claims']['P551'])


    Parameters
    ----------
    claim_list: list
      A list of claim dictionaries representing a Wikidata claim group.
      See `the wikibase JSON data model docs`_ for a description
      of the format.


    .. _the wikibase JSON data model docs: https://www.mediawiki.org/wiki/Wikibase/DataModel/JSON
    """

    def __init__(self, claim_list: types.ClaimList) -> None:
        super(WikidataClaimGroup, self).__init__()
        self._validate_claim_list(claim_list)
        self._claim_list = claim_list
        self._claims = [WikidataClaim(claim_dict) for claim_dict in claim_list]

        property_ids = set([claim.mainsnak.property_id for claim in self._claims])
        self.property_id: Union[types.PropertyId, None]
        if len(property_ids) == 1:
            self.property_id = property_ids.pop()
        elif len(property_ids) == 0:
            self.property_id = None
        else:
            raise ValueError(
                "claims in a claim list must all have the same property id "
                f"but found multiple property ids {property_ids}"
            )

    def _validate_claim_list(self, claim_list: types.ClaimList) -> None:
        """Raise excpetions if claim_list is not valid."""
        if not isinstance(claim_list, list):
            raise TypeError(f"claim_list must be a list but got {type(claim_list)}.")

    @overload
    def __getitem__(self, indx: int) -> WikidataClaim:
        ...

    @overload
    def __getitem__(self, indx: slice) -> List[WikidataClaim]:
        ...

    def __getitem__(self, indx: Union[int, slice]) -> Union[WikidataClaim, List[WikidataClaim]]:
        return self._claims[indx]

    def __len__(self) -> int:
        return len(self._claims)

    def __str__(self) -> str:
        return f"WikidataClaimGroup(property_id={self.property_id}, claims={self._claims})"

    def __repr__(self) -> str:
        return self.__str__()
