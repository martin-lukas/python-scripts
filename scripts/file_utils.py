def rename_file(file_path, new_name):
    try:
        file_path.rename(file_path.with_name(new_name))
        print(f'Renamed {file_path.name} to {new_name}')
    except Exception as e:
        print(f'Error renaming {file_path.name}: {e}')

