to_remove = {
    "xx",
    "a.*.c",
    "y.z",
}

def prepare_to_remove(to_remove):
    to_remove_list = [
        key.split(".")
        for key in to_remove
    ]
    return sorted(to_remove_list, key=lambda x: len(x), reverse=True)



def remove_keys(data, keys_to_remove):
    for key in keys_to_remove:
        data.pop(key, None)
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