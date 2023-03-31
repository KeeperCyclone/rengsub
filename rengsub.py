r"""
module name: rengsub
author: KeeperCyclone
date: 2023-03-31
python version: >= 3.8

purpose: |

    Implements a method for selectively substituting the contents of a matched string
    via named groups defined by a RegEx pattern.

    E.g. If a RegEx pattern is "This (?P<copula>\w+) a string", it is possible to
    replace any string detected as the "copula" so that:

    ```
    >>> ReNamedGroupSub(
    ...         "This (?P<copula>\w+) a string"
    ...     ).__call__(
    ...                 string="This is a string",
    ...                 copula="was"
    ...                ) == "This was a string"

    ```
"""


import re
import typing
import operator


def _splice(
        string: str,
        replacement: typing.Optional[str],
        start: typing.Optional[int] = None,
        stop: typing.Optional[int] = None
        ) -> str:
    """
    Replace the substring, defined by start and stop, in a string with a replacement.

    If an argument is not supplied to start or stop, they will take the start and end index
    of the target string, respectively.

    If no replacement is supplied, the original string is returned unchanged.
    """
    if replacement is None:
        return string
    if start is None:
        start = 0
    if stop is None:
        stop = len(string)
    
    result = f"{string[:start]}{replacement}{string[stop:]}"
    return result


class _Group:
    """
    A data-oriented class containing information about a group
    in a re.Match object.
    """
    __slots__ = ("num", "start", "end", "name")

    def __init__(
            self,
            num: int,
            start: int,
            end: int,
            name: str = ""
            ) -> None:
        self.num = num
        self.start = start
        self.end = end
        self.name = name


def _mirrored(mapping: typing.Mapping) -> dict:
    """
    Mirrors key:value pairs. Throws an exception if
    one-to-one correspondence is violated.
    """
    mirror = {
        mapping[key]: key
        for key
        in mapping.keys()
    }
    return mirror


def _get_groups(m: re.Match) -> typing.List[_Group]:
    """
    Returns a list of Group objects associated with the supplied Match.
    """
    re_pattern = m.re
    mirrored_groupindex = _mirrored(re_pattern.groupindex)
    groupnums = range(1, re_pattern.groups + 1)
    groups = [
        _Group(
            num=i,
            start=m.start(i),
            end=m.end(i),
            name=mirrored_groupindex.get(i, "")
        )
        for i
        in groupnums
    ]

    return groups


class ReNamedGroupSub:
    """
    Core class for substituting the matched contents of named groups of a string.
    Initialized with a string describing a regex pattern.
    """

    def __init__(self, re_pattern: str) -> None:
        self.pattern = re.compile(re_pattern)
    
    def __call__(self, string: str, **subs: str) -> str:
        m = self.pattern.match(string)
        if m is None:
            raise ValueError("No match found.")
        
        groups = _get_groups(m)
        groups.sort(key=operator.attrgetter("num"), reverse=True)

        result = string
        for g in groups:
            result = _splice(
                string=result,
                replacement=subs.get(g.name, None),
                start=g.start,
                stop=g.end
            )

        return result


def sub(re_pattern: str, string: str, **subs: str) -> str:
    """
    Convenience function. Substitute substrings in `string` defined
    by named groups in the given regex pattern. Substitutions are
    defined by the supplied key-value arguments.

    In implementation, creates a new ReNamedGroupSub instance each time
    it is called. If the same re_pattern is expected to be used over and
    over again, please instantiate a ReNamedGroupSub object instead.
    """
    rrn = ReNamedGroupSub(re_pattern=re_pattern)
    return rrn(string=string, **subs)

