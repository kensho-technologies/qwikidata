import json
import os
import unittest

import pytest
from qwikidata import types
from qwikidata.datavalue import WikibaseEntityId
from qwikidata.entity import WikidataItem, WikidataLexeme, WikidataProperty

PATH_HERE = os.path.dirname(os.path.realpath(__file__))
PATH_TO_TEST_DATA = os.path.join(PATH_HERE, "data")

EN = types.LanguageCode("en")
DE = types.LanguageCode("de")
NO = types.LanguageCode("not a language")


def _load_item_dict(item_id: types.ItemId) -> types.ItemDict:
    """Return an item dictionary."""
    fpath = os.path.join(PATH_TO_TEST_DATA, f"wd_{item_id}.json")
    with open(fpath, "r") as fp:
        item_dict = json.load(fp)
    return item_dict


def _load_property_dict(property_id: types.PropertyId) -> types.PropertyDict:
    """Return n property dictionary."""
    fpath = os.path.join(PATH_TO_TEST_DATA, f"wd_{property_id}.json")
    with open(fpath, "r") as fp:
        property_dict = json.load(fp)
    return property_dict


def _load_lexeme_dict(lexeme_id: types.LexemeId) -> types.LexemeDict:
    """Return an lexeme dictionary."""
    fpath = os.path.join(PATH_TO_TEST_DATA, f"wd_{lexeme_id}.json")
    with open(fpath, "r") as fp:
        lexeme_dict = json.load(fp)
    return lexeme_dict


class TestEntityDictExceptions(unittest.TestCase):
    def test_validate_entity_dict_1(self) -> None:
        """Assert TypeError is raised if entity_dict is not a dictionary."""
        entity_dict = "not a dictionary"
        for entity_class in [WikidataItem, WikidataProperty, WikidataLexeme]:
            with pytest.raises(TypeError) as excinfo:
                entity_class(entity_dict)
        assert "_dict must be a dictionary" in str(excinfo.value)

    def test_validate_entity_dict_2(self) -> None:
        """Assert ValueError is raised if entity_dict is missing required keys."""
        entity_dict = dict()  # type: ignore
        for entity_class in [WikidataItem, WikidataProperty, WikidataLexeme]:
            with pytest.raises(ValueError) as excinfo:
                entity_class(entity_dict)
        assert "required entity_dict keys are" in str(excinfo.value)


class TestGetEntityLabel(unittest.TestCase):
    def test_get_label_1(self) -> None:
        """Assert correct behavior in get_label method."""
        q42_dict = _load_item_dict(types.ItemId("Q42"))
        en_label = q42_dict["labels"][EN]["value"]
        de_label = q42_dict["labels"][DE]["value"]
        item = WikidataItem(q42_dict)

        assert item.get_label() == en_label
        assert item.get_label(lang=EN) == en_label
        assert item.get_label(lang=DE) == de_label
        assert item.get_label(lang=NO) == ""

        p279_dict = _load_property_dict(types.PropertyId("P279"))
        en_label = p279_dict["labels"][EN]["value"]
        de_label = p279_dict["labels"][DE]["value"]
        prop = WikidataProperty(p279_dict)

        assert prop.get_label() == en_label
        assert prop.get_label(lang=EN) == en_label
        assert prop.get_label(lang=DE) == de_label
        assert prop.get_label(lang=NO) == ""


class TestGetEntityDescription(unittest.TestCase):
    def test_get_description_1(self) -> None:
        """Assert correct behavior in get_description method."""
        q42_dict = _load_item_dict(types.ItemId("Q42"))
        en_description = q42_dict["descriptions"][EN]["value"]
        de_description = q42_dict["descriptions"][DE]["value"]
        item = WikidataItem(q42_dict)

        assert item.get_description() == en_description
        assert item.get_description(lang=EN) == en_description
        assert item.get_description(lang=DE) == de_description
        assert item.get_description(lang=NO) == ""

        p279_dict = _load_property_dict(types.PropertyId("P279"))
        en_description = p279_dict["descriptions"][EN]["value"]
        de_description = p279_dict["descriptions"][DE]["value"]
        prop = WikidataProperty(p279_dict)

        assert prop.get_description() == en_description
        assert prop.get_description(lang=EN) == en_description
        assert prop.get_description(lang=DE) == de_description
        assert prop.get_description(lang=NO) == ""


class TestGetEntityAliases(unittest.TestCase):
    def test_get_aliases_1(self) -> None:
        """Assert correct behavior in get_aliases method."""
        q42_dict = _load_item_dict(types.ItemId("Q42"))
        en_aliases = [el["value"] for el in q42_dict["aliases"][EN]]
        de_aliases = [el["value"] for el in q42_dict["aliases"][DE]]
        item = WikidataItem(q42_dict)

        assert item.get_aliases() == en_aliases
        assert item.get_aliases(lang=EN) == en_aliases
        assert item.get_aliases(lang=DE) == de_aliases
        assert item.get_aliases(lang=NO) == []

        p279_dict = _load_property_dict(types.PropertyId("P279"))
        en_aliases = [el["value"] for el in p279_dict["aliases"][EN]]
        de_aliases = [el["value"] for el in p279_dict["aliases"][DE]]
        prop = WikidataProperty(p279_dict)

        assert prop.get_aliases() == en_aliases
        assert prop.get_aliases(lang=EN) == en_aliases
        assert prop.get_aliases(lang=DE) == de_aliases
        assert prop.get_aliases(lang=NO) == []


class TestGetClaimGroup(unittest.TestCase):
    def test_get_claim_1(self) -> None:
        """Assert correct behavior."""
        q42_dict = _load_item_dict(types.ItemId("Q42"))
        given_name_douglas = "Q463035"
        given_name_noel = "Q19688263"
        item = WikidataItem(q42_dict)
        claim_group = item.get_claim_group(types.PropertyId("P735"))
        assert len(claim_group) == 2
        given_names = set([cl.mainsnak.datavalue.value["id"] for cl in claim_group])
        assert given_names == set([given_name_douglas, given_name_noel])


class TestGetTruthyClaimGroup(unittest.TestCase):
    def test_get_truthy_claim_1(self) -> None:
        """Assert correct behavior with one preferred and one normal."""
        q42_dict = _load_item_dict(types.ItemId("Q42"))
        given_name_douglas = "Q463035"
        item = WikidataItem(q42_dict)
        truthy_claim_group = item.get_truthy_claim_group(types.PropertyId("P735"))
        assert len(truthy_claim_group) == 1
        claim = truthy_claim_group[0]
        mainsnak = claim.mainsnak
        datavalue = mainsnak.datavalue
        assert isinstance(datavalue, WikibaseEntityId)
        qid = datavalue.value["id"]
        assert qid == given_name_douglas
