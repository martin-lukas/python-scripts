def rename_file(file_path, new_name):
    file_path.rename(file_path.with_name(new_name))
    return file_path.with_name(new_name)
