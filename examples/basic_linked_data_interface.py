from qwikidata.entity import WikidataItem, WikidataLexeme, WikidataProperty
from qwikidata.linked_data_interface import get_entity_dict_from_api

# create an item representing "Douglas Adams"
Q_DOUGLAS_ADAMS = "Q42"
q42_dict = get_entity_dict_from_api(Q_DOUGLAS_ADAMS)
q42 = WikidataItem(q42_dict)

# create a property representing "subclass of"
P_SUBCLASS_OF = "P279"
p279_dict = get_entity_dict_from_api(P_SUBCLASS_OF)
p279 = WikidataProperty(p279_dict)

# create a lexeme representing "bank"
L_BANK = "L3354"
l3354_dict = get_entity_dict_from_api(L_BANK)
l3354 = WikidataLexeme(l3354_dict)
