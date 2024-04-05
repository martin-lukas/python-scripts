from console_utils import print_success, print_error

PREVIOUS_DIR = '..'


def rename_file(file_path, new_name):
    try:
        file_path.rename(file_path.with_name(new_name))
        print_success(f'Renamed {file_path.name} to {new_name}')
    except Exception as e:
        print_error(f'Error renaming {file_path.name}: {e}')

