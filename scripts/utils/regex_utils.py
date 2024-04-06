def get_regex_match(file_name, pattern):
    match = pattern.search(file_name)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid episode file name.")
