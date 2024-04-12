from numdb.misc import merge_dict, flatten_dict, get_first


def test_merge():
    a = {"one": 1, "two": 2}
    b = {"two": 3, "tre": 3}
    assert merge_dict(a, b) == {"two": 2, "tre": 3, "one": 1}


def test_flat():
    nested_dict = {"a": 1, "b": {"c": 2, "d": {"e": 3}}}
    assert flatten_dict(nested_dict) == {"a": 1, "b.c": 2, "b.d.e": 3}


def test_first():
    a = {"one": 1, "two": 2}
    b = {"two": 3, "tre": 3}
    assert get_first("two", a, b) == 2
