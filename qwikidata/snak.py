# Copyright 2019 Kensho Technologies, LLC.
"""Module for Wikidata Snaks."""

from typing import Union

from qwikidata import types
from qwikidata.datavalue import WikidataDatavalue, get_datavalue_from_snak_dict


class WikidataSnak:
    """A Wikidata snak.

    Parameters
    ----------
    snak_dict: dict
      A dictionary representing a Wikidata snak.
      See `the wikibase JSON data model docs`_ for a description
      of the format.


    Attributes
    ----------
    snaktype: str
      One of ["value", "somevalue", "novalue"].  "value" indicates that a known value exists,
      "somevalue" indicates that an unknown value exists, and "novalue" indicates that no
      value exists.
    property_id: str
      A Wikidata property id (e.g. "P551")
    snak_datatype: str or `None`
      The snak data type (SDT). Must be one of ["commonsMedia", "external-id", "geo-shape",
      "globe-coordinate", "math", "monolingualtext", "quantity", "string", "tabular-data", "time",
      "url", "wikibase-item", "wikibase-property", `None`].  Will be `None` if `snaktype` is not
      "value".
    value_datatype: str or `None`
      The value data type (VDT).  Must be one of ["globecoordinate", "monolingualtext",
      "quantity", "string", "time", "wikibase-entityid", `None`].  Will be `None` if `snaktype`
      is not "value".
    datavalue: :py:class:`WikidataDataValue` or `None`
      The datavalue object for this snak.  Has `datatype` and `value` attributes. (this data type
      is the same as VDT above).


    .. note::

      There are two related data types here, the snak data type (SDT) and the value data
      type (VDT).  The SDT is derived from the data type of the property referenced by
      `property_id` and is stored in the `snak_datatype` attribute.  The VDT defines
      the structure of the `value` attribute of :py:class:`WikidataDataValue`.
      The VDT does not allow for interpretation of the datavalue, only for processing of the raw
      structure. As an example, a link to a web page may have SDT="url", but have VDT="string".


    .. _the wikibase JSON data model docs: https://www.mediawiki.org/wiki/Wikibase/DataModel/JSON
    """

    def __init__(self, snak_dict: types.SnakDict) -> None:
        self._validate_snak_dict(snak_dict)
        self._snak_dict = snak_dict

    def _validate_snak_dict(self, snak_dict: types.SnakDict) -> None:
        """Raise excpetions if snak_dict is not valid."""
        _REQUIRED_KEYS = ["snaktype", "property"]
        for req_key in _REQUIRED_KEYS:
            if req_key not in snak_dict:
                raise ValueError(
                    f"required snak_dict keys are {_REQUIRED_KEYS}. "
                    f"only found {list(snak_dict.keys())}"
                )
        self.snaktype = snak_dict["snaktype"]
        self.property_id = snak_dict["property"]

        self.snak_datatype: Union[str, None]
        self.value_datatype: Union[str, None]
        self.datavalue: Union[WikidataDatavalue, None]

        if self.snaktype == "value":
            _REQUIRED_KEYS = ["datavalue", "datatype"]
            for req_key in _REQUIRED_KEYS:
                if req_key not in snak_dict:
                    raise ValueError(
                        f"required snak_dict keys are {_REQUIRED_KEYS}. "
                        f"only found {list(snak_dict.keys())}"
                    )
            self.snak_datatype = snak_dict["datatype"]
            self.value_datatype = str(snak_dict["datavalue"]["type"])
            self.datavalue = get_datavalue_from_snak_dict(snak_dict)

        elif self.snaktype == "somevalue" or self.snaktype == "novalue":
            self.snak_datatype = None
            self.value_datatype = None
            self.datavalue = None

        else:
            raise ValueError(
                f'snaktype must be one of ["value", "somevalue", "novalue"] '
                f"but got {self.snaktype}"
            )

    def __str__(self) -> str:
        return (
            f"WikidataSnak(snaktype={self.snaktype}, property_id={self.property_id}, "
            f"snak_datatype={self.snak_datatype}, value_datatype={self.value_datatype}, "
            f"datavalue={self.datavalue})"
        )

    def __repr__(self) -> str:
        return self.__str__()
