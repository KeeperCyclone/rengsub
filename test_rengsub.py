import rengsub


def test_substitutes_one_named_group():
    rngs = rengsub.ReNamedGroupSub(r"This (?P<copula>\w+) a string")
    assert rngs(string="This is a string", copula="was") == "This was a string"


def test_substitutes_two_named_groups():
    rngs = rengsub.ReNamedGroupSub(r"This (?P<copula>\w+) a (?P<noun>\w+)")
    assert (
        rngs(
            string="This is a string", 
            copula="was",
            noun="str"
        ) == "This was a str"
    )


def test_ungiven_substitution_preserves_original():
    rngs = rengsub.ReNamedGroupSub(r"This (?P<copula>\w+) a (?P<noun>\w+)")
    assert (
        rngs(
            string="This is a string", 
            copula="was",
        ) == "This was a string"
    )


def test_doesnt_do_anything_to_unnamed_groups():
    rngs = rengsub.ReNamedGroupSub(r"This (\w+) a (?P<noun>\w+)")
    assert (
        rngs(
            string="This is a string", 
            noun="str",
        ) == "This is a str"
    )

