from utils import parse_message, split_costs


def test_parse():
    assert parse_message(None) is None
    assert parse_message('lorem') is None
    assert parse_message('lorem 19.99') is None
    assert parse_message('99999') is None
    assert parse_message('-99999') is None
    assert parse_message(1) is None

    assert parse_message('19.99') == 19.99
    assert parse_message('19,99') == 19.99
    assert parse_message('19.99 lorem') == 19.99


def test_split():
    assert split_costs(None) == {}
    assert split_costs({}) == {}
    assert split_costs({'a': 0, 'b': 0}) == {}
    assert split_costs({'a': 10, 'b': 0}) == {'b': {'a': 5}}
    assert split_costs({'a': 0, 'b': 10}) == {'a': {'b': 5}}
    assert split_costs({'a': 10, 'b': 10}) == {}
    assert split_costs({'a': 10.68888, 'b': 0}) == {'b': {'a': 5.34444}}
    assert split_costs({'a': 0, 'b': 10.68888}) == {'a': {'b': 5.34444}}
    assert split_costs({'a': -10, 'b': 10}) == {'a': {'b': 10}}
    assert split_costs({'a': -10, 'b': -10}) == {}

    assert split_costs({'a': 0, 'b': 200, 'c': 100}) == {'a': {'b': 100}}
    assert split_costs({'a': 0, 'b': 100, 'c': 200}) == {'a': {'c': 100}}
    assert split_costs({'a': 100, 'b': 200, 'c': 0}) == {'c': {'b': 100}}
    assert split_costs({'a': 100, 'b': 0, 'c': 200}) == {'b': {'c': 100}}
    assert split_costs({'a': 200, 'b': 100, 'c': 0}) == {'c': {'a': 100}}
    assert split_costs({'a': 200, 'b': 0, 'c': 100}) == {'b': {'a': 100}}

    assert split_costs({'a': 1000, 'b': 0, 'c': 600, 'd': 0}) == \
           {'b': {'a': 400}, 'd': {'a': 200, 'c': 200}}
    assert split_costs({'a': 100, 'b': 100, 'c': 0, 'd': 100, 'e': 100}) == \
           {'c': {'a': 20.0, 'b': 20.0, 'd': 20.0, 'e': 20.0}}
    assert split_costs({'a': 1, 'b': 0, 'c': 1, 'd': 0, 'e': 1, 'f': 0}) == \
           {'b': {'a': 0.5}, 'd': {'c': 0.5}, 'f': {'e': 0.5}}
    assert split_costs({'a': 0, 'b': 1, 'c': 0, 'd': 1, 'e': 0, 'f': 1}) == \
           {'a': {'b': 0.5}, 'c': {'d': 0.5}, 'e': {'f': 0.5}}
