from pathlib import Path
import re
import sys

SEASON_EPISODE_PATTERN = re.compile(r'(S\d{2}E\d{2})')


def process_files(dir_path, tv_show_name):
    try:
        files = [f for f in dir_path.iterdir() if f.is_file()]
        for file in files:
            new_name = clean_episode_name(file.name, tv_show_name)
            rename_file(file, f"{new_name}{file.suffix}")
    except FileNotFoundError:
        print(f"The specified folder '{dir_path}' does not exist.")


def clean_episode_name(name, tv_show_name):
    season_and_episode = SEASON_EPISODE_PATTERN.search(name)
    if season_and_episode:
        return f'{tv_show_name} {season_and_episode.group(1)}'
    else:
        return name


def rename_file(file_path, new_name):
    try:
        file_path.rename(file_path.with_name(new_name))
        print(f'Renamed {file_path.name} to {new_name}')
    except Exception as e:
        print(f'Error renaming {file_path.name}: {e}')


if __name__ == "__main__":
    if len(sys.argv) != 3:  # First parameter is the script name
        print("Usage: python clean_episode_filenames.py <folder> <TV show>")
    else:
        dir_param = sys.argv[1]
        tv_show_param = sys.argv[2]
        process_files(Path(dir_param), tv_show_param)
