from non_fungible_data.json_parser import extract_paths_from_dictionary


def test_extract_paths_from_dictionary():

    data = {'a': 1, 'b': 1, 'c': {'a': [11, 22, 33], 'b': {'111': 111}}}
    assert extract_paths_from_dictionary(data) == ['a', 'b', 'c:a', 'c:b:111']
    assert extract_paths_from_dictionary(data, unfold_sub_iterables=True) == [
        'a',
        'b',
        'c:a::0::',
        'c:a::1::',
        'c:a::2::',
        'c:b:111',
    ]

    data = {'a': 'b'}
    assert extract_paths_from_dictionary(data) == ['a']
    data = {'a': 1, 'b': 1, 'c': {'a': [{11: 1}, 22, 33], 'b': {'111': 111}}}
    assert extract_paths_from_dictionary(data, unfold_sub_iterables=True) == [
        'a',
        'b',
        'c:a::0::11::',
        'c:a::1::',
        'c:a::2::',
        'c:b:111',
    ]

    data = {'a': 1, 1: 'a', 2: {1, 2, 3}}
    assert extract_paths_from_dictionary(data) == ['a', '::1::', '::2::']
    assert extract_paths_from_dictionary(data, unfold_sub_iterables=True) == [
        'a',
        '::1::',
        '::2::0::',
        '::2::1::',
        '::2::2::',
    ]
