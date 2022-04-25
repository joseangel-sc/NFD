from non_fungible_data.json_parser import extract_data_from_route
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

    data = {
        "users": [
            {
                "type": "postData",
                "data": {
                    "postId": "443328e9497740b456154c636349",
                    "postTimestamp": "1521543600",
                    "pageType": "/home.php:topnews",
                    "viewTime": 1521545993647,
                    "gender": 3,
                    "likes": "8",
                    "comments_shares_viewes": ["1"],
                    "posters": [{"type": "page", "id": "695e45affa1e07529ac917f6d573a"}],
                    "postImg": 1,
                    "postDesc": [253],
                    "origLink": 0,
                    "duration": 0,
                    "timestamp": 1521545993647,
                },
                "back_time": 1521545993693,
            },
            {
                "type": "saveLooked",
                "data": {"duration": 18, "timestamp": 1521545993656, "sessionId": 639, "gender": 2},
                "back_time": 1521546011657,
            },
        ]
    }
    expected_routes = [
        'users::0::type',
        'users::0::data:postId',
        'users::0::data:postTimestamp',
        'users::0::data:pageType',
        'users::0::data:viewTime',
        'users::0::data:gender',
        'users::0::data:likes',
        'users::0::data:comments_shares_viewes::0::',
        'users::0::data:posters::0::type',
        'users::0::data:posters::0::id',
        'users::0::data:postImg',
        'users::0::data:postDesc::0::',
        'users::0::data:origLink',
        'users::0::data:duration',
        'users::0::data:timestamp',
        'users::0::back_time',
        'users::1::type',
        'users::1::data:duration',
        'users::1::data:timestamp',
        'users::1::data:sessionId',
        'users::1::data:gender',
        'users::1::back_time',
    ]
    assert extract_paths_from_dictionary(data, unfold_sub_iterables=True) == expected_routes


def test_extract_data_from_route():
    data = {'a': 1, 'b': 1, 'c': {'a': [11, 22, 33], 'b': {'111': 111}}}
    assert extract_data_from_route(data, route='c:a::0::', separator=':') == 11
    assert extract_data_from_route(data, route='c:a::2::', separator=':') == 33
    assert extract_data_from_route(data, route='c:a', separator=':') == [11, 22, 33]

    data = {
        "users": [
            {
                "type": "postData",
                "data": {
                    "postId": "443328e9497740b456154c636349",
                    "postTimestamp": "1521543600",
                    "pageType": "/home.php:topnews",
                    "viewTime": 1521545993647,
                    "gender": 3,
                    "likes": "8",
                    "comments_shares_viewes": ["1"],
                    "posters": [{"type": "page", "id": "695e45affa1e07529ac917f6d573a"}],
                    "postImg": 1,
                    "postDesc": [253],
                    "origLink": 0,
                    "duration": 0,
                    "timestamp": 1521545993647,
                },
                "back_time": 1521545993693,
            },
            {
                "type": "saveLooked",
                "data": {"duration": 18, "timestamp": 1521545993656, "sessionId": 639, "gender": 2},
                "back_time": 1521546011657,
            },
        ]
    }

    routes_and_expected_values = {
        'users::0::type': 'postData',
        'users::0::data:postId': '443328e9497740b456154c636349',
        'users::0::data:postTimestamp': '1521543600',
        'users::0::data:pageType': '/home.php:topnews',
        'users::0::data:viewTime': 1521545993647,
        'users::0::data:gender': 3,
        'users::0::data:likes': '8',
        'users::0::data:comments_shares_viewes::0::': '1',
        'users::0::data:posters::0::type': 'page',
        'users::0::data:posters::0::id': '695e45affa1e07529ac917f6d573a',
        'users::0::data:postImg': 1,
        'users::0::data:postDesc::0::': 253,
        'users::0::data:origLink': 0,
        'users::0::data:duration': 0,
        'users::0::data:timestamp': 1521545993647,
        'users::0::back_time': 1521545993693,
        'users::1::type': 'saveLooked',
        'users::1::data:duration': 18,
        'users::1::data:timestamp': 1521545993656,
        'users::1::data:sessionId': 639,
        'users::1::data:gender': 2,
        'users::1::back_time': 1521546011657,
    }

    for route, expected_result in routes_and_expected_values.items():
        assert extract_data_from_route(data, route, separator=':') == expected_result
