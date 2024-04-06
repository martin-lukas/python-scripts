#!/Users/martin/code/python/venv/bin/python

import os
import re
import shutil
from pathlib import Path

from console_utils import *
from file_utils import rename_file
from regex_utils import get_regex_match

TORRENTS_PATH = os.path.expanduser('~/Downloads/Torrents')
JELLYFIN_PATH = os.path.expanduser('~/Movies')
FILM = {
    'name': 'Film', 'folder': os.path.join(JELLYFIN_PATH, 'Films')
}
TV_SHOW = {
    'name': 'TV show', 'folder': os.path.join(JELLYFIN_PATH, 'TV Shows')
}
MEDIA_TYPES = [FILM, TV_SHOW]
SEASON_EPISODE_PATTERN = re.compile(r'(S\d{2}E\d{2})')
PREVIOUS_DIR = '..'


# --- Custom exceptions ---
class MediaAlreadyExists(Exception):
    pass


# --- Console input functions ---
def read_media_type():
    def choose_media_type():
        while True:
            print_choices([media['name'] for media in MEDIA_TYPES])
            choice = read("> ")
            if choice.isdigit() and 0 < int(choice) <= len(MEDIA_TYPES):
                return int(choice) - 1
            else:
                print_error("Invalid choice. Try again.")
    
    print("Which media type is it?")
    choice = choose_media_type()
    return MEDIA_TYPES[choice]


def read_year():
    return read_number(
        "Year: ", lambda x: 1900 <= x <= 2030, "Invalid year. Try again."
    )


def read_tv_show_season():
    return read_number(
        "Season: ", lambda x: 1 <= x <= 100, "Invalid season. Try again."
    )


# --- Logic functions ---
def find_file(history, cur_path):
    def choose_file(choices):
        while True:
            print_choices(choices)
            choice = read("> ")
            if (
                choice.isdigit() and 1 <= int(choice) <= len(choices)
            ) or choice == "":
                return choice
            else:
                print_error("Invalid choice. Try again.")
    
    files = [f for f in os.listdir(cur_path) if not f.startswith(".")]
    if len(history) > 0:
        files.insert(0, PREVIOUS_DIR)
    
    choice = choose_file(files)
    if choice == "":
        # Choose current folder
        return Path(cur_path)
    elif choice.isdigit():
        chosen_file = files[int(choice) - 1]
        if chosen_file == PREVIOUS_DIR:
            # Go back to previous folder
            return find_file(history[:-1], history[-1])
        else:
            chosen_path = os.path.join(cur_path, chosen_file)
            if os.path.isdir(chosen_path):
                # Explore selected folder
                history.append(cur_path)
                return find_file(history, chosen_path)
            else:
                # Choose selected file
                return Path(chosen_path)


def rename_film_files(torrent_path, media_name):
    if torrent_path.is_dir():
        files = [f for f in torrent_path.iterdir() if f.is_file()]
        for file in files:
            rename_file(file, media_name)
    else:
        raise ValueError("Invalid folder path (a file).")


def move_film(torrent_path, media_name, year):
    film_folder_name = f"{media_name} ({year})"
    try:
        film_folder = os.path.join(FILM['folder'], film_folder_name)
        os.makedirs(film_folder)
        if torrent_path.is_dir():
            for file in os.listdir(torrent_path):
                shutil.move(
                    os.path.join(torrent_path, file),
                    os.path.join(film_folder, file)
                )
        else:
            shutil.move(
                torrent_path, os.path.join(film_folder, torrent_path.name)
            )
    except FileExistsError:
        raise MediaAlreadyExists(film_folder_name)


def rename_episode_files(dir_path, tv_show_name):
    files = [f for f in dir_path.iterdir() if f.is_file()]
    if files:
        for file in files:
            season_episode = get_regex_match(file.name, SEASON_EPISODE_PATTERN)
            rename_file(file, f"{tv_show_name} {season_episode}")


def move_tv_show_season(torrent_path, media_name, year, season):
    tv_show_folder = os.path.join(TV_SHOW['folder'], f"{media_name} ({year})")
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
        torrent_path = find_file(history=[], cur_path=TORRENTS_PATH)
        chosen_media_type = read_media_type()
        media_name = read(f"{chosen_media_type['name']} name: ")
        year = read_year()
        if chosen_media_type == FILM:
            if torrent_path.is_dir():
                rename_film_files(torrent_path, media_name)
                move_film(torrent_path, media_name, year)
            else:
                new_film_path = rename_file(torrent_path, media_name)
                move_film(new_film_path, media_name, year)
        elif chosen_media_type == TV_SHOW:
            rename_episode_files(torrent_path, media_name)
            season = read_tv_show_season()
            move_tv_show_season(torrent_path, media_name, year, season)
        print_success("Media moved successfully.")
    except MediaAlreadyExists as e:
        print_error(f"Media '{e}' already exists.")
    except KeyboardInterrupt:
        print("\nExiting...")
        exit(1)
