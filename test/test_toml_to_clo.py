import pytest
from cloacal.toml_to_clo import toml2clo


def test_toml2clo_basic():
    toml_input = """
    name = "Carlisle"
    age = 99
    species = "seagull"
    ilk = "bird"

    description = """
    Id ipsum elit tempor non incididunt laborum 
    anim dolore eu fugiat.
    """

    memories = [
        "Consectetur ut qui Lorem ad.",
        "Veniam mollit nostrud velit laborum veniam irure ut aute magna labore aliqua."
    ]
    """

    expected_output = """
+----------------------------------------+
|                Carlisle                |
+----------------------------------------+

age ------- 99
ilk ------- bird
species --- seagull

description -------------------------------
  Id ipsum elit tempor non incididunt laborum 
  anim dolore eu fugiat.

memories ----------------------------------
  > Consectetur ut qui Lorem ad.
  > Veniam mollit nostrud velit laborum veniam irure ut aute magna labore aliqua.
""".strip()

    formatted_output = toml2clo(toml_input)
    assert formatted_output == expected_output


def test_toml2clo_missing_fields():
    toml_input = """
    name = "Anonymous"
    age = 30
    species = "human"

    description = """
    This is a character with some missing fields.
    """
    """

    expected_output = """
+----------------------------------------+
|               Anonymous                 |
+----------------------------------------+

age ------- 30
species --- human

description -------------------------------
  This is a character with some missing fields.
""".strip()

    formatted_output = toml2clo(toml_input)
    assert formatted_output == expected_output


def test_toml2clo_empty_input():
    toml_input = ""
    expected_output = ""
    formatted_output = toml2clo(toml_input)
    assert formatted_output == expected_output


def test_toml2clo_additional_fields():
    toml_input = """
    name = "Evelyn"
    age = 28
    species = "fox"
    ilk = "clever"
    occupation = "detective"

    description = """
    A clever fox with a knack for solving mysteries.
    """

    skills = [
        "stealth",
        "investigation",
        "disguise"
    ]
    """

    expected_output = """
+----------------------------------------+
|                 Evelyn                 |
+----------------------------------------+

age ------- 28
ilk ------- clever
occupation -- detective
species --- fox

description -------------------------------
  A clever fox with a knack for solving mysteries.

skills -----------------------------------
  > stealth
  > investigation
  > disguise
""".strip()

    formatted_output = toml2clo(toml_input)
    assert formatted_output == expected_output


def test_toml2clo_invalid_toml():
    toml_input = """
    name = "Invalid
    age = thirty
    species = "dragon"
    """

    with pytest.raises(tomllib.TOMLDecodeError):
        toml2clo(toml_input)
