from utils import parse_message, split_costs


def test_parse_invalid():
    assert parse_message("lorem") is None


def test_parse_valid():
    assert parse_message("19.99") == 19.99
    assert parse_message("19.99 lorem") == 19.99


def test_split_costs():
    assert split_costs({}) == {}
    assert split_costs({"a": 0, "b": 0}) == {}
    assert split_costs({"a": 10, "b": 0}) == {"b": {"a": 5}}
    assert split_costs({"a": 250, "b": 50, "c": 0}) == {"b": {"a": 50}, "c": {"a": 100}}
    assert split_costs({"a": 1000, "b": 0, "c": 600, "d": 0}) == {"b": {"a": 400}, "d": {"a": 200, "c": 200}}
