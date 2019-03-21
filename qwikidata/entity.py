# Copyright 2019 Kensho Technologies, LLC.
"""Module for Wikidata Entities."""

from typing import Dict, List, Union

from qwikidata import types
from qwikidata.claim import WikidataClaimGroup


class EntityMixin:
    """Mixin for all entities.

    .. seealso::

        * :py:class:`WikidataItem`
        * :py:class:`WikidataProperty`
        * :py:class:`WikidataLexeme`

    """

    @staticmethod
    def _validate_entity_dict(entity_dict: types.EntityDict) -> None:
        """Raise excpetions if entity_dict is not valid."""
        _REQUIRED_KEYS = ["id", "type"]
        if not isinstance(entity_dict, dict):
            raise TypeError(f"entity_dict must be a dictionary but got {type(entity_dict)}.")
        for req_key in _REQUIRED_KEYS:
            if req_key not in entity_dict:
                raise ValueError(
                    f"required entity_dict keys are {_REQUIRED_KEYS}. "
                    f"only found {list(entity_dict.keys())}"
                )


class LabelDescriptionAliasMixin:
    """Mixin for entities with labels, descriptions, and aliases.

    .. seealso::

        * :py:class:`WikidataItem`
        * :py:class:`WikidataProperty`

    """

    _entity_dict: types.EntityDict

    @staticmethod
    def _validate_label_desc_alias_dict(
        label_desc_alias_dict: Union[types.ItemDict, types.PropertyDict]
    ) -> None:
        """Raise excpetions if label_desc_alias_dict is not valid."""
        _REQUIRED_KEYS = ["labels", "descriptions", "aliases"]
        for req_key in _REQUIRED_KEYS:
            if req_key not in label_desc_alias_dict:
                raise ValueError(
                    f"required label_desc_alias_dict keys are {_REQUIRED_KEYS}. "
                    f"only found {list(label_desc_alias_dict.keys())}"
                )

    def get_label(self, lang: types.LanguageCode = types.LanguageCode("en")) -> str:
        """Get label (primary name for this entity) in a specific language.

        See: https://www.wikidata.org/wiki/Help:Label

        Parameters
        ----------
        lang
          Find the label in this language.
        """
        if isinstance(self._entity_dict["labels"], dict) and lang in self._entity_dict["labels"]:
            return self._entity_dict["labels"][lang]["value"]
        else:
            return ""

    def get_description(self, lang: types.LanguageCode = types.LanguageCode("en")) -> str:
        """Get a brief description of this entity in a specific language.

        See: https://www.wikidata.org/wiki/Help:Description

        Parameters
        ----------
        lang
          Find the description in this language.
        """
        if (
            isinstance(self._entity_dict["descriptions"], dict)
            and lang in self._entity_dict["descriptions"]
        ):
            return self._entity_dict["descriptions"][lang]["value"]
        else:
            return ""

    def get_aliases(self, lang: types.LanguageCode = types.LanguageCode("en")) -> List[str]:
        """Get alternative names for this entity in a specific language.

        See: https://www.wikidata.org/wiki/Help:Aliases

        Parameters
        ----------
        lang
          Find aliases in this language.
        """
        if isinstance(self._entity_dict["aliases"], dict) and lang in self._entity_dict["aliases"]:
            return [el["value"] for el in self._entity_dict["aliases"][lang]]
        else:
            return []


class ClaimsMixin:
    """Mixin for entities with top level claims (aka statements).

    See: https://www.wikidata.org/wiki/Help:Statements

    .. seealso::

        * :py:class:`WikidataItem`
        * :py:class:`WikidataProperty`
        * :py:class:`WikidataLexeme`
        * :py:class:`WikidataForm`
        * :py:class:`WikidataSense`
    """

    _entity_dict: types.EntityDict

    @staticmethod
    def _validate_claim_dict(claim_dict: types.EntityDict) -> None:
        """Raise excpetions if claim_dict is not valid."""
        _REQUIRED_KEYS = ["claims"]
        for req_key in _REQUIRED_KEYS:
            if req_key not in claim_dict:
                raise ValueError(
                    f"required claim_dict keys are {_REQUIRED_KEYS}. "
                    f"only found {list(claim_dict.keys())}"
                )

    def get_claim_groups(self) -> Dict[types.PropertyId, WikidataClaimGroup]:
        """Get all claim groups about this entity."""
        if isinstance(self._entity_dict["claims"], dict):
            claims = {
                property_id: WikidataClaimGroup(claim_list)
                for property_id, claim_list in self._entity_dict["claims"].items()
            }
            return claims
        else:
            return {}

    def get_claim_group(self, property_id: types.PropertyId) -> WikidataClaimGroup:
        """Get the claim group corresponding to a given property id.

        Parameters
        ----------
        property_id
            the string representing the property ID of the claim group to return
        """
        if not isinstance(self._entity_dict["claims"], dict):
            return WikidataClaimGroup([])

        claim_list = self._entity_dict["claims"].get(property_id, None)
        if claim_list is None:
            return WikidataClaimGroup([])
        else:
            return WikidataClaimGroup(claim_list)

    def get_truthy_claim_groups(self) -> Dict[types.PropertyId, WikidataClaimGroup]:
        """Get all truthy claim groups about this entity.

        Truthy is defined in the Wikidata RDF dump format docs,

            "Truthy statements represent statements that have the best non-deprecated rank for a
            given property. Namely, if there is a preferred statement for a property P, then only
            preferred statements for P will be considered truthy. Otherwise, all normal-rank
            statements for P are considered truthy."

            -- `RDF dump format docs on truthy statements`_


        .. _RDF dump format docs on truthy statements: https://www.mediawiki.org/wiki/Wikibase/Indexing/RDF_Dump_Format#Truthy_statements
        """
        if isinstance(self._entity_dict["claims"], dict):
            claims = {}
            property_ids = self._entity_dict["claims"].keys()
            for property_id in property_ids:
                claims[property_id] = self.get_truthy_claim_group(property_id)
            return claims
        else:
            return {}

    def get_truthy_claim_group(self, property_id: types.PropertyId) -> WikidataClaimGroup:
        """Get truthy claims from the claim group corresponding to a given property id.

        Truthy is defined in the Wikidata RDF dump format docs,

            "Truthy statements represent statements that have the best non-deprecated rank for a
            given property. Namely, if there is a preferred statement for a property P, then only
            preferred statements for P will be considered truthy. Otherwise, all normal-rank
            statements for P are considered truthy."

            -- `RDF dump format docs on truthy statements`_


        Parameters
        ----------
        property_id
            the string representing the property ID of the claim group to return


        .. _RDF dump format docs on truthy statements: https://www.mediawiki.org/wiki/Wikibase/Indexing/RDF_Dump_Format#Truthy_statements
        """
        claim_group = self.get_claim_group(property_id)

        truthy_claim_dicts = [
            claim._claim_dict for claim in claim_group if claim.rank.lower() == "preferred"
        ]

        if len(truthy_claim_dicts) == 0:
            truthy_claim_dicts = [
                claim._claim_dict for claim in claim_group if claim.rank.lower() != "deprecated"
            ]

        return WikidataClaimGroup(truthy_claim_dicts)


class WikidataItem(LabelDescriptionAliasMixin, ClaimsMixin, EntityMixin):
    """Class for Wikidata Items.

    Parameters
    ----------
    item_dict
      A dictionary representation of a Wikidata Item.
      See `the wikibase JSON data model docs`_ for a description
      of the dictionary format.


    .. seealso::

      Wikidata docs on items,

        * https://www.wikidata.org/wiki/Help:Items


      Ways to generate item dictionaries within qwikidata.

        * :py:class:`qwikidata.json_dump.WikidataJsonDump`
        * :py:func:`qwikidata.linked_data_interface.get_entity_dict_from_api`


    .. _the wikibase JSON data model docs: https://www.mediawiki.org/wiki/Wikibase/DataModel/JSON
    """

    def __init__(self, item_dict: types.ItemDict) -> None:
        self._validate_item_dict(item_dict)
        self._entity_dict = item_dict
        self.entity_id = item_dict["id"]
        self.entity_type = item_dict["type"]

    def _validate_item_dict(self, item_dict: types.ItemDict) -> None:
        """Raise excpetions if item_dict is not valid."""
        self._validate_entity_dict(item_dict)
        if item_dict["type"] != "item":
            raise ValueError(f"item_dict['type'] must be 'item' but found '{item_dict['type']}'")
        self._validate_label_desc_alias_dict(item_dict)
        self._validate_claim_dict(item_dict)

    def get_sitelinks(self, prefix: str = "enwiki") -> Dict[str, types.SitelinkDict]:
        """Get Wikimedia sitelinks for this item.

        Parameters
        ----------
        prefix
          filters to sitelinks that begin with `prefix`.  can filter by language (e.g. "en")
          or by language and site (e.g. "enwiki").

        Returns
        -------
        dict
          A dictionary with site names as keys and sitelink dictionaries as values.
        """
        if isinstance(self._entity_dict["sitelinks"], dict):
            return {k: v for k, v in self._entity_dict["sitelinks"].items() if k.startswith(prefix)}
        else:
            return {}

    def get_enwiki_title(self) -> str:
        """Get english language wikipedia page title."""
        if (
            isinstance(self._entity_dict["sitelinks"], dict)
            and "enwiki" in self._entity_dict["sitelinks"]
        ):
            return self._entity_dict["sitelinks"]["enwiki"]["title"]
        else:
            return ""

    def __str__(self) -> str:
        return "WikidataItem(label={}, id={}, description={}, aliases={}, enwiki_title={})".format(
            self.get_label(),
            self.entity_id,
            self.get_description(),
            self.get_aliases(),
            self.get_enwiki_title(),
        )

    def __repr__(self) -> str:
        return self.__str__()


class WikidataProperty(LabelDescriptionAliasMixin, ClaimsMixin, EntityMixin):
    """Class for Wikidata Properties.

    Parameters
    ----------
    property_dict
      A dictionary representation of a Wikidata Property.
      See `the wikibase JSON data model docs`_ for a description
      of the dictionary format.


    .. seealso::

      Wikidata docs on properties,

        * https://www.wikidata.org/wiki/Help:Properties


      Ways to generate property dictionaries within kwikimedia.

        * :py:class:`qwikidata.json_dump.WikidataJsonDump`
        * :py:func:`qwikidata.linked_data_interface.get_entity_dict_from_api`


    .. _the wikibase JSON data model docs: https://www.mediawiki.org/wiki/Wikibase/DataModel/JSON
    """

    def __init__(self, property_dict: types.PropertyDict) -> None:
        self._validate_property_dict(property_dict)
        self._entity_dict = property_dict
        self.entity_id = property_dict["id"]
        self.entity_type = property_dict["type"]

    def _validate_property_dict(self, property_dict: types.PropertyDict) -> None:
        """Raise excpetions if property_dict is not valid."""
        self._validate_entity_dict(property_dict)
        if property_dict["type"] != "property":
            raise ValueError(
                f"property_dict['type'] must be 'property' but found '{property_dict['type']}'"
            )
        self._validate_label_desc_alias_dict(property_dict)
        self._validate_claim_dict(property_dict)

    def __str__(self) -> str:
        return "WikidataProperty(label={}, id={}, description={}, aliases={})".format(
            self.get_label(), self.entity_id, self.get_description(), self.get_aliases()
        )

    def __repr__(self) -> str:
        return self.__str__()


class WikidataForm(ClaimsMixin):
    """A form associated with a Wikidata Lexeme.

    See: https://www.mediawiki.org/wiki/Extension:WikibaseLexeme/Data_Model#Form

    This class can be initialized from a lexeme dictionary as,

    .. code-block:: python

      >>> form_dict = l3354_dict['forms'][0]
      >>> wikidata_form = WikidataForm(form_dict)


    Parameters
    ----------
    form_dict
      A dictionary representing a Wikidata Lexeme form.


    Attributes
    ----------
    form_id: str
      Unique id for this form (e.g. 'L3354-F1')
    grammatical_features: list
      List of item ids representing grammatical categories (e.g. present tense, first person, ...)
    """

    def __init__(self, form_dict: types.FormDict) -> None:
        self._validate_form_dict(form_dict)
        self._form_dict = form_dict

        self.form_id = form_dict["id"]
        self.grammatical_features = form_dict["grammaticalFeatures"]

    def _validate_form_dict(self, form_dict: types.FormDict) -> None:
        """Raise excpetions if form_dict is not valid."""
        _REQUIRED_KEYS = ["id", "representations", "grammaticalFeatures", "claims"]
        for req_key in _REQUIRED_KEYS:
            if req_key not in form_dict:
                raise ValueError(
                    f"required form_dict keys are {_REQUIRED_KEYS}. "
                    f"only found {list(form_dict.keys())}"
                )

    def get_representation(self, lang: types.LanguageCode = types.LanguageCode("en")) -> str:
        """Get representation of this form in a given language.

        See: https://www.mediawiki.org/wiki/Extension:WikibaseLexeme/Data_Model#Representation

        Parameters
        ----------
        lang
          Find the representation in this language.
        """
        if (
            isinstance(self._form_dict["representations"], dict)
            and lang in self._form_dict["representations"]
        ):
            return self._form_dict["representations"][lang]["value"]
        else:
            return ""

    def __str__(self) -> str:
        return f"WikidataForm(form_id={self.form_id}, representation={self.get_representation()}, grammatical_features={self.grammatical_features}"

    def __repr__(self) -> str:
        return self.__str__()


class WikidataSense(ClaimsMixin):
    """A sense associated with a Wikidata Lexeme.

    See: https://www.mediawiki.org/wiki/Extension:WikibaseLexeme/Data_Model#Sense

    This class can be initialized from a lexeme dictionary as,

    .. code-block:: python

      >>> sense_dict = l3354_dict['senses'][0]
      >>> wikidata_sense = WikidataSense(sense_dict)


    Parameters
    ----------
    sense_dict
      A dictionary representing a Wikidata Lexeme sense.


    Attributes
    ----------
    sense_id: str
      Unique id for this sense (e.g. 'L3354-S1')
    """

    def __init__(self, sense_dict: types.SenseDict) -> None:
        self._validate_sense_dict(sense_dict)
        self._sense_dict = sense_dict

        self.sense_id = sense_dict["id"]

    def _validate_sense_dict(self, sense_dict: types.SenseDict) -> None:
        """Raise excpetions if sense_dict is not valid."""
        _REQUIRED_KEYS = ["id", "glosses", "claims"]
        for req_key in _REQUIRED_KEYS:
            if req_key not in sense_dict:
                raise ValueError(
                    f"required sense_dict keys are {_REQUIRED_KEYS}. "
                    f"only found {list(sense_dict.keys())}"
                )

    def get_gloss(self, lang: types.LanguageCode = types.LanguageCode("en")) -> str:
        """Get gloss of this sense in a given language.

        See: https://www.mediawiki.org/wiki/Extension:WikibaseLexeme/Data_Model#Gloss

        Parameters
        ----------
        lang
          Find the gloss in this language.
        """
        if isinstance(self._sense_dict["glosses"], dict) and lang in self._sense_dict["glosses"]:
            return self._sense_dict["glosses"][lang]["value"]
        else:
            return ""

    def __str__(self) -> str:
        return f"WikidataSense(sense_id={self.sense_id}, gloss={self.get_gloss()}"

    def __repr__(self) -> str:
        return self.__str__()


class WikidataLexeme(ClaimsMixin, EntityMixin):
    """Class for Wikidata Lexeme.

    Parameters
    ----------
    lexeme_dict
      A dictionary representation of a Wikidata Lexeme.
      See `the wikibase Lexeme JSON data model docs`_ for a description
      of the dictionary format.


    .. seealso::

      Wikidata docs on lexemes,

        * https://www.wikidata.org/wiki/Wikidata:Lexicographical_data


      Ways to generate lexeme dictionaries within qwikidata.

        * :py:class:`qwikidata.json_dump.WikidataJsonDump`
        * :py:func:`qwikidata.linked_data_interface.get_entity_dict_from_api`


    .. _the wikibase Lexeme JSON data model docs: https://www.mediawiki.org/wiki/Extension:WikibaseLexeme/Data_Model
    """

    def __init__(self, lexeme_dict: types.LexemeDict) -> None:
        self._validate_lexeme_dict(lexeme_dict)
        self._entity_dict: types.LexemeDict = lexeme_dict
        self.entity_id = lexeme_dict["id"]
        self.entity_type = lexeme_dict["type"]
        self.language = lexeme_dict["language"]
        self.lexical_category = lexeme_dict["lexicalCategory"]

    def _validate_lexeme_dict(self, lexeme_dict: types.LexemeDict) -> None:
        """Raise excpetions if lexeme_dict is not valid."""
        self._validate_entity_dict(lexeme_dict)
        if lexeme_dict["type"] != "lexeme":
            raise ValueError(
                f"lexeme_dict['type'] must be 'lexeme' but found '{lexeme_dict['type']}'"
            )
        self._validate_claim_dict(lexeme_dict)

        _REQUIRED_KEYS = ["lemmas", "lexicalCategory", "language", "forms", "senses"]

        for req_key in _REQUIRED_KEYS:
            if req_key not in lexeme_dict:
                raise ValueError(
                    f"required lexeme_dict keys are  {_REQUIRED_KEYS}. "
                    f"only found {list(lexeme_dict.keys())}"
                )

    def get_lemma(self, lang: types.LanguageCode = types.LanguageCode("en")) -> str:
        """Get lemma (primary name for this lexeme) in a specific language.

        See: https://www.mediawiki.org/wiki/Extension:WikibaseLexeme/Data_Model#Lemma

        Parameters
        ----------
        lang
          Find the lemma in this language.
        """
        if isinstance(self._entity_dict["lemmas"], dict) and lang in self._entity_dict["lemmas"]:
            return self._entity_dict["lemmas"][lang]["value"]
        else:
            return ""

    def get_forms(self) -> List[WikidataForm]:
        """Get the set of forms assocaited with this Lexeme."""
        return [WikidataForm(form_dict) for form_dict in self._entity_dict["forms"]]

    def get_senses(self) -> List[WikidataSense]:
        """Get the set of senses assocaited with this Lexeme."""
        return [WikidataSense(sense_dict) for sense_dict in self._entity_dict["senses"]]

    def __str__(self) -> str:
        return "WikidataLexeme(lemma={}, id={}, language={}, lexical_category={}, forms={}, senses={})".format(
            self.get_lemma(),
            self.entity_id,
            self.language,
            self.lexical_category,
            self.get_forms(),
            self.get_senses(),
        )

    def __repr__(self) -> str:
        return self.__str__()
