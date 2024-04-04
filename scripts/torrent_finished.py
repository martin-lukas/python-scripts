#!/Users/martin/code/python/venv/bin/python

import os
import shutil
from pathlib import Path
import re

from console_utils import print_error, read, \
    print_success, print_choices
from file_utils import rename_file

DOWNLOADS_PATH = os.path.expanduser('~/Downloads/Torrents')
JELLYFIN_PATH = os.path.expanduser('~/Movies')
FILM = {
    'name': 'Film',
    'folder': os.path.join(JELLYFIN_PATH, 'Films')
}
TV_SHOW = {
    'name': 'TV show',
    'folder': os.path.join(JELLYFIN_PATH, 'TV Shows')
}
MEDIA_TYPES = [FILM, TV_SHOW]
SEASON_EPISODE_PATTERN = re.compile(r'(S\d{2}E\d{2})')


class TorrentFolderEmpty(Exception):
    pass


def find_file(prev_path=None, cur_path=None):
    files = [f for f in os.listdir(cur_path) if not f.startswith(".")]
    if not files:
        raise TorrentFolderEmpty("No files found in the folder.")
    
    def choose_with_default(choices, prompt, error_message):
        while True:
            print_choices(choices)
            choice = read(prompt)
            if choice.isdigit() and 0 < int(choice) <= len(choices):
                return int(choice) - 1
            elif choice == "":
                return -1
            else:
                print_error(error_message)
    
    choice = choose_with_default(files, "> ", "Invalid choice. Try again.")
    if choice != -1:
        chosen_path = os.path.join(cur_path, files[choice])
        if os.path.isdir(chosen_path):
            # Explore selected folder
            return find_file(cur_path, chosen_path)
        else:
            # Choose selected file
            return Path(chosen_path)
    else:
        # Choose current folder
        return Path(cur_path)


def read_media_type():
    print("Which media type is it?")
    
    def choose(choices, prompt, error_message):
        while True:
            print_choices(choices)
            choice = read(prompt)
            if choice.isdigit() and 0 < int(choice) <= len(choices):
                return int(choice) - 1
            else:
                print_error(error_message)
    
    choice = choose(
        [media['name'] for media in MEDIA_TYPES],
        "> ",
        "Invalid choice. Try again."
    )
    return MEDIA_TYPES[choice]


def clean_film_filenames(torrent_path, media_name):
    files = [f for f in torrent_path.iterdir() if f.is_file()]
    if files:
        for file in files:
            rename_file(file, f"{media_name}{file.suffix}")


def move_film(torrent_path, media_name):
    try:
        film_folder = os.path.join(FILM['folder'], media_name)
        os.makedirs(film_folder)
        for file in os.listdir(torrent_path):
            shutil.move(
                os.path.join(torrent_path, file),
                os.path.join(film_folder, file)
            )
    except FileExistsError:
        print_error(f"{media_name} already exists.")


def clean_episode_filenames(dir_path, tv_show_name):
    files = [f for f in dir_path.iterdir() if f.is_file()]
    if files:
        for file in files:
            new_name = clean_episode_name(file.name, tv_show_name)
            rename_file(file, f"{new_name}{file.suffix}")


def clean_episode_name(name, tv_show_name):
    season_and_episode = SEASON_EPISODE_PATTERN.search(name)
    if season_and_episode:
        return f'{tv_show_name} {season_and_episode.group(1)}'
    else:
        return name


def move_tv_show_season(torrent_path, media_name):
    season = read("Season: ")
    
    tv_show_folder = os.path.join(TV_SHOW['folder'], media_name)
    os.makedirs(tv_show_folder, exist_ok=True)
    season_folder = os.path.join(tv_show_folder, f"Season {season.zfill(2)}")
    try:
        os.makedirs(season_folder)
        for episode in os.listdir(torrent_path):
            shutil.move(
                os.path.join(torrent_path, episode),
                os.path.join(season_folder, episode)
            )
    except FileExistsError:
        print_error(f"Season {season} already exists.")


if __name__ == "__main__":
    print("Which media do you want to move to Jellyfin?")
    try:
        try:
            torrent_path = find_file(cur_path=DOWNLOADS_PATH)
            chosen_media_type = read_media_type()
            media_name = read(f"{chosen_media_type['name']} name: ")
            if chosen_media_type == TV_SHOW:
                clean_episode_filenames(torrent_path, media_name)
                move_tv_show_season(torrent_path, media_name)
            else:
                clean_film_filenames(torrent_path, media_name)
                move_film(torrent_path, media_name)
            print_success("Media moved successfully.")
        except TorrentFolderEmpty:
            print_error("No files found in the selected folder.")
            exit(1)
    except KeyboardInterrupt:
        print("\nExiting...")
        exit(1)
