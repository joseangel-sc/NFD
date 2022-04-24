def extract_paths_from_dictionary(data: dict, current_path: str = '', separator: str = ':') -> list:
    routes = []
    if not data:
        return routes
    if current_path and current_path[-1] != separator:
        current_path += separator
    for key, value in data.items():
        next_path = f"{current_path}{key}"
        if isinstance(value, dict):
            routes += extract_paths_from_dictionary(value, next_path, separator)
        else:
            routes += [next_path]

    return routes
