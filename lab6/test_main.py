import pytest
from pydantic import ValidationError
from main import Block, Person, Vote, DataLoader


@pytest.fixture
def real_loader():
    """Підключається до твоєї реальної бази даних"""
    loader = DataLoader("voting_system.db")
    yield loader
    loader.close()


def test_person_validation():
    p = Person(id=10, name="Oleg", addr="Kyiv")
    assert p.id == 10

def test_block_id_pattern():
    with pytest.raises(ValidationError):
        Block(id="343595-91-30", view=0)


def test_get_existing_block(real_loader):
    block = Block.get_by_id(real_loader, "0x5a2f")
    if block:
        assert block.id == "0x5a2f"
        assert isinstance(block.view, int)
    else:
        pytest.skip("Блоку 0x5a2f немає в базі")

def test_find_name_in_db(real_loader):
    results = Person.find_by_name(real_loader, "Ivan")
    assert isinstance(results, list)
    if len(results) > 0:
        assert isinstance(results[0], Person)


def test_person_name_too_short():
    with pytest.raises(ValidationError):
        Person(id=1, name="A", addr="Lviv")

def test_block_view_negative():
    with pytest.raises(ValidationError):
        Block(id="0x123abc", view=-5)



def test_find_non_existent_person(real_loader):
    results = Person.find_by_name(real_loader, "Zyxwvut123")
    assert isinstance(results, list)
    assert len(results) == 0

def test_get_votes_for_empty_block(real_loader):
    votes = Vote.get_votes_for_block(real_loader, "0x999999")
    assert votes == []