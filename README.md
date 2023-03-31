# rengsub
A Python module for selectively substituting the contents of a matched string via named groups defined by a RegEx pattern.

E.g. If a RegEx pattern is "This (?P<copula>\w+) a string", it is possible to
replace any string detected as the "copula" so that:

```python

>>> rengsub.ReNamedGroupSub(
...         "This (?P<copula>\w+) a string"
...     ).__call__(
...                 string="This is a string",
...                 copula="was"
...               ) == "This was a string"

```

Or use the convenience function:

```python

>>> rengsub.sub(
...     re_pattern="This (?P<copula>\w+) a string",
...     string="This is a string",
...     copula="was"
... ) == "This was a string"

```

