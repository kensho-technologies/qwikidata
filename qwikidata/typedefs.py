# Copyright 2019 Kensho Technologies, LLC.
"""Module providing Wikidata Types."""
from typing import Dict, List, NewType, Union

from mypy_extensions import TypedDict

# Ids
# ====================================================
ItemId = NewType("ItemId", str)
PropertyId = NewType("PropertyId", str)
LexemeId = NewType("LexemeId", str)
EntityId = Union[ItemId, PropertyId, LexemeId]

NumericItemId = NewType("NumericItemId", int)
NumericPropertyId = NewType("NumericPropertyId", int)
NumericLexemeId = NewType("NumericLexemeId", int)
NumericEntityId = Union[NumericItemId, NumericPropertyId, NumericLexemeId]

FormId = NewType("FormId", str)
SenseId = NewType("SenseId", str)


# Named strings
# ====================================================
EntityUri = NewType("EntityUri", str)
LanguageCode = NewType("LanguageCode", str)


# Datavalues
# ====================================================
GlobeCoordinateValue = TypedDict(
    "GlobeCoordinateValue",
    {"latitude": float, "longitude": float, "precision": float, "globe": EntityUri},
)
GlobeCoordinateDatavalueDict = TypedDict(
    "GlobeCoordinateDatavalueDict", {"type": str, "value": GlobeCoordinateValue}
)

MonolingualTextValue = TypedDict("MonolingualTextValue", {"text": str, "language": LanguageCode})
MonolingualTextDatavalueDict = TypedDict(
    "MonolingualTextDatavalueDict", {"value": MonolingualTextValue, "type": str}
)

QuantityValue = TypedDict(
    "QuantityValue", {"amount": str, "upperBound": str, "lowerBound": str, "unit": str}
)
QuantityDatavalueDict = TypedDict("QuantityDatavalueDict", {"value": QuantityValue, "type": str})

StringValue = NewType("StringValue", str)
StringDatavalueDict = TypedDict("StringDatavalueDict", {"value": StringValue, "type": str})

TimeValue = TypedDict(
    "TimeValue",
    {
        "time": str,
        "timezone": int,
        "calendarmodel": EntityUri,
        "precision": int,
        "before": int,
        "after": int,
    },
)
TimeDatavalueDict = TypedDict("TimeDatavalueDict", {"value": TimeValue, "type": str})

WikibaseEntityIdValue = TypedDict(
    "WikibaseEntityIdValue", {"entity-type": str, "id": EntityId, "numeric-id": NumericEntityId}
)
WikibaseEntityIdDatavalueDict = TypedDict(
    "WikibaseEntityIdDatavalueDict", {"value": WikibaseEntityIdValue, "type": str}
)

WikibaseUnmappedEntityIdValue = NewType("WikibaseUnmappedEntityIdValue", str)
WikibaseUnmappedEntityIdDatavalueDict = TypedDict(
    "WikibaseUnmappedEntityIdDatavalueDict", {"value": WikibaseUnmappedEntityIdValue, "type": str}
)


DatavalueDict = Union[
    GlobeCoordinateDatavalueDict,
    MonolingualTextDatavalueDict,
    QuantityDatavalueDict,
    StringDatavalueDict,
    TimeDatavalueDict,
    WikibaseEntityIdDatavalueDict,
    WikibaseUnmappedEntityIdDatavalueDict,
]


# Snak
# ====================================================
SnakDict = TypedDict(
    "SnakDict",
    {"snaktype": str, "property": PropertyId, "datatype": str, "datavalue": DatavalueDict},
)

# Claims
# ====================================================
ReferenceDict = TypedDict(
    "ReferenceDict",
    {"hash": str, "snaks": Dict[PropertyId, List[SnakDict]], "snaks-order": List[PropertyId]},
)

QualifierDict = TypedDict(
    "QualifierDict",
    {
        "hash": str,
        "snaktype": str,
        "property": PropertyId,
        "datatype": str,
        "datavalue": DatavalueDict,
    },
)

ClaimDict = TypedDict(
    "ClaimDict",
    {
        "id": str,
        "mainsnak": SnakDict,
        "type": str,
        "rank": str,
        "qualifiers": Dict[PropertyId, List[QualifierDict]],
        "references": List[ReferenceDict],
        "qualifiers-order": List[PropertyId],
    },
)

ClaimList = List[ClaimDict]


# Items and Properties
# ====================================================
LabelDict = TypedDict("LabelDict", {"language": LanguageCode, "value": str})

DescriptionDict = TypedDict("DescriptionDict", {"language": LanguageCode, "value": str})

AliasDict = TypedDict("AliasDict", {"language": LanguageCode, "value": str})

AliasList = List[AliasDict]

SitelinkDict = TypedDict(
    "SitelinkDict", {"site": str, "title": str, "badges": List[str], "url": str}
)

ItemDict = TypedDict(
    "ItemDict",
    {
        "pageid": int,
        "ns": int,
        "title": str,
        "lastrevid": int,
        "modified": str,
        "type": str,
        "id": ItemId,
        "labels": Dict[LanguageCode, LabelDict],
        "descriptions": Dict[LanguageCode, DescriptionDict],
        "aliases": Dict[LanguageCode, AliasList],
        "sitelinks": Dict[str, SitelinkDict],
        "claims": Dict[PropertyId, ClaimList],
    },
)

PropertyDict = TypedDict(
    "PropertyDict",
    {
        "pageid": int,
        "ns": int,
        "title": str,
        "lastrevid": int,
        "modified": str,
        "type": str,
        "id": PropertyId,
        "labels": Dict[LanguageCode, LabelDict],
        "descriptions": Dict[LanguageCode, DescriptionDict],
        "aliases": Dict[LanguageCode, AliasList],
        "claims": Dict[PropertyId, ClaimList],
    },
)


# Lexemes
# ====================================================
RepresentationDict = TypedDict("RepresentationDict", {"language": LanguageCode, "value": str})

FormDict = TypedDict(
    "FormDict",
    {
        "id": FormId,
        "representations": Dict[LanguageCode, RepresentationDict],
        "grammaticalFeatures": List[ItemId],
        "claims": Dict[PropertyId, ClaimList],
    },
)


GlossDict = TypedDict("GlossDict", {"language": LanguageCode, "value": str})

SenseDict = TypedDict(
    "SenseDict",
    {
        "id": SenseId,
        "glosses": Dict[LanguageCode, GlossDict],
        "claims": Dict[PropertyId, ClaimList],
    },
)

LemmaDict = TypedDict("LemmaDict", {"language": LanguageCode, "value": str})

LexemeDict = TypedDict(
    "LexemeDict",
    {
        "pageid": int,
        "ns": int,
        "title": str,
        "lastrevid": int,
        "modified": str,
        "type": str,
        "id": LexemeId,
        "lemmas": Dict[LanguageCode, LemmaDict],
        "lexicalCategory": ItemId,
        "language": ItemId,
        "claims": Dict[PropertyId, ClaimList],
        "forms": List[FormDict],
        "senses": List[SenseDict],
    },
)

EntityDict = Union[ItemDict, PropertyDict, LexemeDict]
