import pytest

from model.card_game.suit import Suit
from model.card_game.value import Value
from model.card_game.card import Card


@pytest.fixture(scope="class")
def seven_of_spades():
    return Card(Value.SEVEN, Suit.SPADES)


@pytest.mark.usefixtures("seven_of_spades")
class TestCardClass:

    def test_description_facedown(self, seven_of_spades):
        assert seven_of_spades.description(False) == "Facedown card"

    def test_description_faceup_ignore(self, seven_of_spades):
        assert seven_of_spades.description(True) == "Seven of Spades"
