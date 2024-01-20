import os
import re
import sys

SEASON_EPISODE_PATTERN = re.compile(r'(S\d{2}E\d{2})')


def clean_episode_name(full_filename, tv_show_name):
    season_and_episode = SEASON_EPISODE_PATTERN.search(full_filename)
    if season_and_episode:
        _, extension = os.path.splitext(full_filename)
        return f'{tv_show_name} {season_and_episode.group(1)}{extension}'
    else:
        return full_filename


def rename_file(dir_path, old_name, new_name):
    try:
        os.rename(
            os.path.join(dir_path, old_name),
            os.path.join(dir_path, new_name)
        )
        print(f'Renamed {old_name} to {new_name}')
    except Exception as e:
        print(f'Error renaming {old_name}: {e}')


def process_files(dir_path, tv_show_name):
    try:
        files = [
            f for f in os.listdir(dir_path)
            if os.path.isfile(os.path.join(dir_path, f))
        ]
        for file in files:
            rename_file(dir_path, file, clean_episode_name(file, tv_show_name))
    except FileNotFoundError:
        print(f"The specified folder '{dir_path}' does not exist.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python clean_episode_filenames.py <folder> <TV show>")
    else:
        work_dir = sys.argv[1]
        tv_show_name = sys.argv[2]
        process_files(work_dir, tv_show_name)
