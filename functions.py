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
        if len(single_key_to_remove) == 1:
            data.pop(first_key, None)
        elif isinstance(data[first_key], dict):
            _remove_keys(data[first_key], single_key_to_remove[1:])


def remove_keys(data, keys_to_remove):
    for key in keys_to_remove:
        _remove_keys(data, key)
    return data


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
