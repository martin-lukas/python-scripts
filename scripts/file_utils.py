from console_utils import print_success, print_error

PREVIOUS_DIR = '..'


def rename_file(file_path, new_name):
    file_path.rename(file_path.with_name(new_name))
