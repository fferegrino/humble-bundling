to_remove = {
    "xx",
    "a.*.c",
    "y.z",
}


def prepare_to_remove(to_remove):
    to_remove_list = [key.split(".") for key in to_remove]
    return sorted(to_remove_list, key=lambda x: len(x), reverse=True)


def _remove_keys(data, single_key_to_remove):
    if isinstance(single_key_to_remove, str):
        data.pop(single_key_to_remove, None)
    elif isinstance(single_key_to_remove, list):
        first_key = single_key_to_remove[0]
        if first_key == "[]" and isinstance(data, list):
            for item in data:
                _remove_keys(item, single_key_to_remove[1:])
        elif first_key == "*" and isinstance(data, dict):
            for key, value in data.items():
                _remove_keys(value, single_key_to_remove[1:])
        elif len(single_key_to_remove) == 1:
            data.pop(first_key, None)
        elif isinstance(data[first_key], dict):
            _remove_keys(data[first_key], single_key_to_remove[1:])
        elif isinstance(data[first_key], list):
            _remove_keys(data[first_key], single_key_to_remove[1:])


def remove_keys(data, keys_to_remove):
    for key in keys_to_remove:
        _remove_keys(data, key)
    return data


def test_arbitrary_dict_keys():
    input = {
        "a": {
            "b1": {
                "hello": "world",
                "c": 1,
            },
            "b2": {
                "hello": "world",
                "c": 2,
            },
            "b3": {
                "hello": "world",
                "d": 2,
            },
        }
    }

    expected = {
        "a": {
            "b1": {"hello": "world"},
            "b2": {"hello": "world"},
            "b3": {"hello": "world", "d": 2},
        }
    }

    actual = remove_keys(input, [["a", "*", "c"]])

    assert actual == expected
    assert expected == input


def test_with_list_level():
    input = {
        "a": [
            {"b": 1},
            {"c": 2},
        ]
    }
    expected = {
        "a": [
            {"b": 1},
            {},
        ]
    }
    actual = remove_keys(input, [["a", "[]", "c"]])

    assert actual == expected
    assert expected == input


def test_simple_one_level():
    input = {
        "a": 1,
        "b": 2,
        "c": 3,
    }
    expected = {
        "a": 1,
        "b": 2,
    }
    actual = remove_keys(input, ["c"])

    assert actual == expected
    assert expected == input


def test_simple_two_level():
    input = {
        "a": {
            "b": 2,
            "c": 3,
        }
    }
    expected = {
        "a": {
            "b": 2,
        }
    }
    actual = remove_keys(input, [["a", "c"]])

    assert actual == expected
    assert expected == input


def test_simple_three_level():
    input = {
        "a": {
            "b": {
                "c": 3,
            }
        },
        "d": 4,
    }
    expected = {
        "a": {"b": {}},
        "d": 4,
    }
    actual = remove_keys(input, [["a", "b", "c"]])

    assert actual == expected
    assert expected == input
