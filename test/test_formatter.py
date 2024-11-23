from cloacal.format import format_str


def test_format_basic_input():
    ugly_input = """
    +--+
    | Carlisle |
    +-----

    age -- 99
    species - seagull
    ilk ------------ bird

    description ----
         Id ipsum elit tempor non incididunt laborum
      anim dolore eu fugiat. Dolor consectetur aute occaecat. Ex do reprehenderit nulla sunt dolor
      laborum qui. Qui voluptate tempor excepteur
      ex ea excepteur. Ipsum do elit fugiat laboris
      veniam pariatur.

    memories -----------------------
      >    Consectetur ut qui Lorem ad.
      >  Veniam mollit nostrud velit laborum laborum veniam irure ut aute magna labore aliqua.
      > 	 Magna reprehenderit anim esse aliquip magna do reprehenderit pariatur laborum do dolor.
    """

    expected_output = """
+------------------------------------------+
|                 Carlisle                 |
+------------------------------------------+

age ------- 99
ilk ------- bird
species --- seagull

description -------------------------------
  Id ipsum elit tempor non incididunt
  laborum anim dolore eu fugiat. Dolor
  consectetur aute occaecat. Ex do
  reprehenderit nulla sunt dolor laborum
  qui. Qui voluptate tempor excepteur ex ea
  excepteur. Ipsum do elit fugiat laboris
  veniam pariatur.

memories ----------------------------------
  > Consectetur ut qui Lorem ad.
  > Veniam mollit nostrud velit laborum
    laborum veniam irure ut aute magna
    labore aliqua.
  > Magna reprehenderit anim esse aliquip
    magna do reprehenderit pariatur laborum
    do dolor.
""".strip()

    formatted_output = format_str(ugly_input)
    assert formatted_output == expected_output


def test_format_missing_name():
    ugly_input = """
    age -- 30
    species - human

    description ----
         A character with no name box.
    """

    expected_output = """
age ------- 30
species --- human

description -------------------------------
  A character with no name box.
""".strip()

    formatted_output = format_str(ugly_input)
    assert formatted_output == expected_output


def test_format_empty_input():
    ugly_input = ""

    expected_output = ""

    formatted_output = format_str(ugly_input)
    assert formatted_output == expected_output


def test_format_only_name():
    ugly_input = """
    +--+
    | Solo |
    +-----
    """

    expected_output = """
+------------------------------------------+
|                   Solo                   |
+------------------------------------------+
""".strip()

    formatted_output = format_str(ugly_input)
    assert formatted_output == expected_output


def test_format_unexpected_content():
    ugly_input = """
    +--+
    | Random |
    +-----

    age -- 22
    unknown_field **** data

    description ----
         Contains unexpected content.
    """

    expected_output = """
+------------------------------------------+
|                  Random                  |
+------------------------------------------+

age ------------- 22
description ----- Contains unexpected content.
unknown_field --- data
""".strip()

    formatted_output = format_str(ugly_input)
    assert formatted_output == expected_output


def test_format_long_name():
    ugly_input = """
    +--+
    | The Great and Powerful Name |
    +-----

    age -- 100
    species - mythical creature
    """

    expected_output = """
+-----------------------------------------+
|       The Great and Powerful Name       |
+-----------------------------------------+

age ------- 100
species --- mythical creature
""".strip()

    formatted_output = format_str(ugly_input)
    assert formatted_output == expected_output


def test_format_block_without_content():
    ugly_input = """
    +--+
    | EmptyBlock |
    +-----

    age --- 30

    description ----

    memories ----
    """

    expected_output = """
+------------------------------------------+
|                EmptyBlock                |
+------------------------------------------+

age ----------- 30
description ---
memories ------
""".strip()

    formatted_output = format_str(ugly_input)
    assert formatted_output == expected_output


def test_format_multiple_blocks():
    ugly_input = """
    +--+
    | MultiBlock |
    +-----

    abilities ----------------------
      Strength, Agility, Intelligence

    inventory ----------------------
      > Sword
      > Shield
      > Potion

    notes --------------------------
      This character has multiple block sections.
    """

    expected_output = """
+------------------------------------------+
|                MultiBlock                |
+------------------------------------------+

abilities --- Strength, Agility, Intelligence

inventory ---------------------------------
  > Sword
  > Shield
  > Potion

notes -------------------------------------
  This character has multiple block
  sections.
""".strip()

    formatted_output = format_str(ugly_input)
    assert formatted_output == expected_output
