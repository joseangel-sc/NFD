from collections.abc import Iterable


def extract_paths_from_dictionary(
    data: dict, current_path: str = '', separator: str = ':', unfold_sub_iterables=False
) -> list:
    routes = []
    if not data:
        return routes
    if current_path and current_path[-1] != separator:
        current_path += separator
    for key, value in data.items():
        if isinstance(key, int):
            key = f"{separator * 2}{key}{separator * 2}"
        next_path = f"{current_path}{key}"
        next_path = _clean_multiple_separators(next_path, separator)
        if isinstance(value, dict):
            routes += extract_paths_from_dictionary(value, next_path, separator, unfold_sub_iterables)
        elif isinstance(value, Iterable) and not isinstance(value, str) and unfold_sub_iterables:
            routes += _extract_sub_iterables(value, separator, next_path)
        else:
            routes += [next_path]

    return routes


def _extract_sub_iterables(value, separator, next_path) -> list:
    routes = []
    for i, item in enumerate(value):
        iter_path = f"{next_path}{separator * 2}{i}{separator * 2}"
        iter_path = _clean_multiple_separators(iter_path, separator)
        if isinstance(item, dict):
            routes += extract_paths_from_dictionary(item, iter_path, separator, unfold_sub_iterables=True)
        else:
            routes += [iter_path]

    return routes


def _clean_multiple_separators(route: str, separator: str) -> str:
    """dumb but i'm lazy and don't want to overthink tis rn, also, I suck at regex"""
    noise = separator * 3
    while noise in route:
        route = route.replace(noise, separator * 2)

    return route


def extract_data_from_route(data: dict, route: str, separator: str):
    """
    In case we actually want NFD to do the extraction of the data itself (and not the db)
    """
    extracted_data = data
    split_route = route.split(separator)
    types = _find_types(route, separator)
    for i, key in enumerate(split_route):
        if types[i] == 'numeric':
            extracted_data = extracted_data[int(key)]
        elif key:
            extracted_data = extracted_data[key]

    return extracted_data


def _find_types(route, separator):
    split_route = ['dummy'] + route.split(separator) + ['dummy']
    types = dict()
    counter = 0
    for prev, curr, next_ in zip(split_route, split_route[1:], split_route[2:]):
        if not prev and not next_:
            types[counter] = 'numeric'
        else:
            types[counter] = 'string'
        counter += 1

    return types
