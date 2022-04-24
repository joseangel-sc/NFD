from non_fungible_data.json_parser import extract_paths_from_dictionary


def test_extract_paths_from_dictionary():
    sample_1 = {'a': 1, 'b': 1, 'c': {'a': [11, 22, 33], 'b': {'111': 111}}}

    assert extract_paths_from_dictionary(sample_1) == ['a', 'b', 'c:a', 'c:b:111']
