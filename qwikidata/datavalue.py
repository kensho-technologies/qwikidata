# Copyright 2019 Kensho Technologies, LLC.
"""Module for Wikidata Datavalues."""

import re
from typing import Dict, Union

from qwikidata import types


def _validate_datavalue_dict(datavalue_dict: types.DatavalueDict) -> None:
    """Raise excpetions if datavalue_dict is not valid."""
    _REQUIRED_KEYS = ["type", "value"]
    for req_key in _REQUIRED_KEYS:
        if req_key not in datavalue_dict:
            raise ValueError(
                f"required datavalue_dict keys are {_REQUIRED_KEYS}. "
                f"only found {list(datavalue_dict.keys())}"
            )

    _VALID_TYPES = frozenset(
        [
            "globecoordinate",
            "monolingualtext",
            "quantity",
            "string",
            "time",
            "wikibase-entityid",
            "wikibase-unmapped-entityid",
        ]
    )
    if datavalue_dict["type"] not in _VALID_TYPES:
        raise ValueError(
            f"datavalue datatype={datavalue_dict['type']} not in "
            f"valid datatypes {_VALID_TYPES}."
        )


class GlobeCoordinate:
    """Class for `globecoordinate` datavalues.

    In this class, the `value` attribute is a mapping with the following keys,

    * **latitude** (`float` or `str`): the latitude part of the coordinate in degrees
    * **longitude** (`float` or `str`): the longitude part of the coordinate in degrees
    * **precision** (`float` or `str`): the coordinate's precision, in (fractions of)
      degrees
    * **globe** (`str`): the URI of a reference globe. This would typically refer to a
      data item on wikidata.org. This is usually just an indication of the celestial body
      (e.g. Q2 = earth), but could be more specific, like WGS 84 or ED50.
    * **altitude** (`float` or `str`): Deprecated and no longer used. Will be dropped in the future.


    Attributes
    ----------
    value: dict
      mapping that represents a location on a globe
    datatype: str
      `globecoordinate`
    """

    def __init__(self, datavalue_dict: types.GlobeCoordinateDatavalueDict) -> None:
        _validate_datavalue_dict(datavalue_dict)
        self._datavalue_dict = datavalue_dict
        self.datatype = datavalue_dict["type"]
        self.value = datavalue_dict["value"]

    def __str__(self) -> str:
        return "GlobeCoordinate(latitude={}, longitude={})".format(
            self.value["latitude"], self.value["longitude"]
        )


class MonolingualText:
    """Class for `monolingualtext` datavalues.

    In this class, the `value` attribute is a mapping with the following keys,

    * **text** (`str`): a string literal
    * **language** (`str`): a `Wikidata language code`_


    .. _Wikidata language code: https://www.wikidata.org/wiki/Help:Wikimedia_language_codes/lists/all


    Attributes
    ----------
    value: dict
      mapping that represents text in a specific language
    datatype: str
      `monolingualtext`
    """

    def __init__(self, datavalue_dict: types.MonolingualTextDatavalueDict) -> None:
        _validate_datavalue_dict(datavalue_dict)
        self._datavalue_dict = datavalue_dict
        self.datatype = datavalue_dict["type"]
        self.value = datavalue_dict["value"]

    def __str__(self) -> str:
        return "MongolingualText(text={}, language={})".format(
            self.value["text"], self.value["language"]
        )


class Quantity:
    """Class for `quantity` datavalues.

    In this class, the `value` attribute is a mapping with the following keys,

    * **amount** (`str`): The nominal value of the quantity, as an arbitrary precision decimal
      string. The string always starts with a character indicating the sign of the value, either
      "+" or "-".
    * **upperBound** (`str`): Optionally, the upper bound of the quantity's uncertainty interval,
      using the same notation as the amount field. If not given or null, the uncertainty (or
      precision) of the quantity is not known. If the upperBound field is given, the lowerBound
      field must also be given.
    * **lowerBound** (`str`): Optionally, the lower bound of the quantity's uncertainty interval,
      using the same notation as the amount field. If not given or null, the uncertainty (or
      precision) of the quantity is not known. If the lowerBound field is given, the upperBound
      field must also be given.
    * **unit** (`str`): the URI of a unit (or "1" to indicate a unit-less quantity). This would
      typically refer to a data item on wikidata.org, e.g. http://www.wikidata.org/entity/Q712226
      for "square kilometer".


    Attributes
    ----------
    value: dict
      mapping that represents a numeric quantity
    datatype: str
      `quantity`
    """

    def __init__(self, datavalue_dict: types.QuantityDatavalueDict) -> None:
        _validate_datavalue_dict(datavalue_dict)
        self._datavalue_dict = datavalue_dict
        self.datatype = datavalue_dict["type"]
        self.value = datavalue_dict["value"]

    def __str__(self) -> str:
        return "Quantity(amount={}, unit={})".format(self.value["amount"], self.value["unit"])


class String:
    """Class for `string` datavalues.

    Attributes
    ----------
    value: str
      a string literal
    datatype: str
      `string`
    """

    def __init__(self, datavalue_dict: types.StringDatavalueDict) -> None:
        _validate_datavalue_dict(datavalue_dict)
        self._datavalue_dict = datavalue_dict
        self.datatype = datavalue_dict["type"]
        self.value = datavalue_dict["value"]

    def __str__(self) -> str:
        return "String(value={})".format(self.value)


class Time:
    """Class for `time` datavalues.

    In this class, the `value` attribute is a mapping with the following keys,

    * **time** (`str`): the format and interpretation of this string depends on the calendar model.
      Currently, only Julian and Gregorian dates are supported.  The format used for Gregorian
      and Julian dates use a notation resembling ISO 8601. E.g. "+1994-01-01T00:00:00Z". The
      year is represented by at least four digits, zeros are added on the left side as needed.
      Years BCE are represented as negative numbers, using the historical numbering, in which
      year 0 is undefined, and the year 1 BCE is represented as -0001, the year 44 BCE is
      represented as -0044, etc., like XSD 1.0 (ISO 8601:1988) does.
      Month and day may be 00 if they are unknown or insignificant. The day of the month
      may have values between 0 and 31 for any month, to accommodate "leap dates" like February
      30. Hour, minute, and second are currently unused and should always be 00.

    * **timezone** (`int`): Signed integer. Currently unused, and should always be 0.

    * **calendarmodel** (`str`): URI of a calendar model, such as gregorian or julian. Typically
      given as the URI of a data item on the repository

    * **precision** (`int`): To what unit is the given date/time significant? Given as an integer
      indicating one of the following units:

        * 0: 1 Gigayear
        * 1: 100 Megayears
        * 2: 10 Megayears
        * 3: Megayear
        * 4: 100 Kiloyears
        * 5: 10 Kiloyears
        * 6: Kiloyear
        * 7: 100 years
        * 8: 10 years
        * 9: years
        * 10: months
        * 11: days
        * 12: hours (unused)
        * 13: minutes (unused)
        * 14: seconds (unused)

      Note that the precision should be read as an indicator of the significant parts of the date
      string, it does not directly specify an interval. That is, 1988-07-13T00:00:00 with
      precision 8 (decade) will be interpreted as 198?-??-?? and rendered as "1980s".
      1981-01-21T00:00:00 with precision 8 would have the exact same interpretation. Thus the two
      dates are equivalent, since year, month, and days are treated as insignificant.

    * **before** (`int`): Beginning of an uncertainty range, given in the unit defined by the
      precision field. This cannot be used to represent a duration. (Currently unused, may be
      dropped in the future)

    * **after** (`int`): End of an uncertainty range, given in the unit defined by the precision
      field. This cannot be used to represent a duration. (Currently unused, may be dropped in the
      future)


    Attributes
    ----------
    value: dict
      mapping that represents a time
    datatype: str
      `time`
    """

    def __init__(self, datavalue_dict: types.TimeDatavalueDict) -> None:
        _validate_datavalue_dict(datavalue_dict)
        self._datavalue_dict = datavalue_dict
        self.datatype = datavalue_dict["type"]
        self.value = datavalue_dict["value"]
        self.STANDARD_DATE_REGEX = re.compile(
            r"""
            (?P<year>[+-]?\d+?)-
            (?P<month>\d\d)-
            (?P<day>\d\d)T
            (?P<hour>\d\d):
            (?P<minute>\d\d):
            (?P<second>\d\d)Z?""",
            re.VERBOSE,
        )

    def __str__(self) -> str:
        return "Time(time={}, precision={})".format(self.value["time"], self.value["precision"])

    def get_parsed_datetime_dict(self) -> Dict[str, int]:
        """Return a dictionary representation of the datavalue.

        Given a Wikidata time string, extract the year, month, and day.

        Time strings look like this, for examples: '+1838-01-01T00:00:00Z'.

        See: https://www.wikidata.org/wiki/Help:Dates

        TODO: Handle truncated dates (like 20 for 20th century)
        TODO: Allow for partial match if we only know some information like the year

        Returns
        -------
        dict
            a dictionary representing the timestring's year, month, and date
        """
        datetime_dict: Dict[str, int] = {}
        timestring = self.value["time"]
        match = self.STANDARD_DATE_REGEX.fullmatch(timestring)
        if match:

            datetime_dict = {
                "year": int(match.group("year")),
                "month": int(match.group("month")),
                "day": int(match.group("day")),
                "hour": int(match.group("hour")),
                "minute": int(match.group("minute")),
                "second": int(match.group("second")),
            }

        return datetime_dict


class WikibaseEntityId:
    """Class for `wikibase-entityid` datavalues.

    In this class, the `value` attribute is a mapping with the following keys,

      * **entity-type** (`str`): one of ["item", "property"]
      * **id** (`str`): string form of entity id (e.g. "Q42")
      * **numeric-id** (`int`): integer form of entity id (e.g. 42)

    Attributes
    ----------
    value: dict
      mapping that references a Wikidata entity
    datatype: str
      `wikibase-entityid`
    """

    def __init__(self, datavalue_dict: types.WikibaseEntityIdDatavalueDict) -> None:
        _validate_datavalue_dict(datavalue_dict)
        self._datavalue_dict = datavalue_dict
        self.datatype = datavalue_dict["type"]
        self.value = datavalue_dict["value"]

    def __str__(self) -> str:
        return "WikibaseEntityId(id={})".format(self.value["id"])


class WikibaseUnmappedEntityId:
    """Class for `wikibase-unmapped-entityid` datavalues.

    In this class, the `value` attribute is a string representing an
    unmapped wikibase entity id.

    Attributes
    ----------
    value: str
      string that references an unmapped entity id
    datatype: str
      `wikibase-unmapped-entityid`
    """

    def __init__(self, datavalue_dict: types.WikibaseUnmappedEntityIdDatavalueDict) -> None:
        _validate_datavalue_dict(datavalue_dict)
        self._datavalue_dict = datavalue_dict
        self.datatype = datavalue_dict["type"]
        self.value = datavalue_dict["value"]

    def __str__(self) -> str:
        return "WikibaseUnmappedEntityId(value={})".format(self.value)


_DATAVALUE_TYPE_TO_CLASS = {
    "globecoordinate": GlobeCoordinate,
    "monolingualtext": MonolingualText,
    "quantity": Quantity,
    "string": String,
    "time": Time,
    "wikibase-entityid": WikibaseEntityId,
    "wikibase-unmapped-entityid": WikibaseUnmappedEntityId,
}


WikidataDatavalue = Union[
    GlobeCoordinate,
    MonolingualText,
    Quantity,
    String,
    Time,
    WikibaseEntityId,
    WikibaseUnmappedEntityId,
]


def get_datavalue_from_snak_dict(snak_dict: types.SnakDict) -> Union[WikidataDatavalue, None]:
    """Return a Wikidata Datavalue from a snak dictionary."""
    if snak_dict["snaktype"] == "value":
        datavalue_class = _DATAVALUE_TYPE_TO_CLASS[str(snak_dict["datavalue"]["type"])]
        return datavalue_class(snak_dict["datavalue"])
    elif snak_dict["snaktype"] == "somevalue" or snak_dict["snaktype"] == "novalue":
        return None
    else:
        raise ValueError(
            f'snaktype must be one of ["value", "somevalue", "novalue"] '
            f"but got {snak_dict['snaktype']}"
        )
