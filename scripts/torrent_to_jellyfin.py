#!/Users/martin/code/python/venv/bin/python
import os
import re
import shutil
from pathlib import Path

from utils.console_utils import *
from utils.file_utils import rename_file
from utils.regex_utils import get_regex_match

TORRENTS_PATH = os.path.expanduser("~/Downloads/Torrents")
JELLYFIN_PATH = os.path.expanduser("~/Movies")
FILM = {
    "name": "Film", "folder": os.path.join(JELLYFIN_PATH, "Films")
}
TV_SHOW = {
    "name": "TV show", "folder": os.path.join(JELLYFIN_PATH, "TV Shows")
}
MEDIA_TYPES = [FILM, TV_SHOW]
SEASON_EPISODE_PATTERN = re.compile(r"(S\d{2}E\d{2})")
PREVIOUS_DIR = ".."


# --- Custom exceptions ---
class MediaAlreadyExists(Exception):
    pass


# --- Console input functions ---
def read_media_type():
    print("Which media type is it?")
    print_choices([media["name"] for media in MEDIA_TYPES])
    choice = read(
        prompt="> ",
        matches=lambda x: x.isdigit() and 1 <= int(x) <= len(MEDIA_TYPES),
        error_message="Invalid choice. Try again."
    )
    return MEDIA_TYPES[int(choice) - 1]


def read_year():
    return read_number(
        "Year: ", lambda x: 1900 <= x <= 2030, "Invalid year. Try again."
    )


def read_tv_show_season():
    return read_number(
        "Season: ", lambda x: 1 <= x <= 100, "Invalid season. Try again."
    )


# --- Logic functions ---
def find_folder(history, cur_path):
    files = [f for f in os.listdir(cur_path) if not f.startswith(".")]
    if len(history) > 0:
        files.insert(0, PREVIOUS_DIR)
    
    print_choices(files)
    choice = read(
        prompt="> ",
        matches=lambda x: x.isdigit() and 1 <= int(x) <= len(files) or x == "",
        error_message="Invalid choice. Try again."
    )
    if choice == "":
        # Choose current folder
        return cur_path
    elif choice.isdigit():
        chosen_file = files[int(choice) - 1]
        if chosen_file == PREVIOUS_DIR:
            # Go back to previous folder
            return find_folder(history[:-1], history[-1])
        else:
            chosen_path = os.path.join(cur_path, chosen_file)
            if os.path.isdir(chosen_path):
                history.append(cur_path)
                # Explore selected folder
                return find_folder(history, chosen_path)
            else:
                print_error("Choose a folder.")
                # Retry
                return find_folder(history, cur_path)


def is_film_in_jellyfin(media_name, year):
    return os.path.exists(
        os.path.join(FILM["folder"], f"{media_name} ({year})")
    )


def transfer_film_to_jellyfin(
    torrent_path, jellyfin_film_path, film_name, year
):
    files = [f for f in Path(torrent_path).iterdir() if f.is_file()]
    for file in files:
        rename_file(file, film_name)
    film_folder_name = f"{film_name} ({year})"
    try:
        film_folder = os.path.join(jellyfin_film_path, film_folder_name)
        os.makedirs(film_folder)
        for file in os.listdir(torrent_path):
            shutil.move(
                src=os.path.join(torrent_path, file),
                dst=os.path.join(film_folder, file)
            )
        shutil.rmtree(torrent_path)
    except FileExistsError:
        raise MediaAlreadyExists(film_folder_name)


def is_tv_show_season_in_jellyfin(media_name, year, season):
    tv_show_folder = f"{media_name} ({year})"
    season_folder = f"Season {str(season).zfill(2)}"
    tv_show_season_folder = os.path.join(
        TV_SHOW["folder"], tv_show_folder, season_folder
    )
    if os.path.exists(tv_show_season_folder):
        raise MediaAlreadyExists(f"{tv_show_folder}/{season_folder}")


def transfer_tv_show_season_to_jellyfin(
    torrent_season_path, jellyfin_tv_show_path, tv_show, year, season
):
    files = [f for f in Path(torrent_season_path).iterdir() if f.is_file()]
    if files:
        for file in files:
            season_episode = get_regex_match(file.name, SEASON_EPISODE_PATTERN)
            rename_file(file, f"{tv_show} {season_episode}")
    season_folder = os.path.join(
        jellyfin_tv_show_path,
        f"{tv_show} ({year})",
        f"Season {str(season).zfill(2)}"
    )
    os.makedirs(season_folder)
    for episode in os.listdir(torrent_season_path):
        shutil.move(
            src=os.path.join(torrent_season_path, episode),
            dst=os.path.join(season_folder, episode)
        )
    shutil.rmtree(torrent_season_path)


def main():
    print("Which media do you want to move to Jellyfin?")
    try:
        torrent_path = find_folder(history=[], cur_path=TORRENTS_PATH)
        chosen_media_type = read_media_type()
        media_name = read("Name: ")
        year = read_year()
        if chosen_media_type == FILM:
            if is_film_in_jellyfin(media_name, year):
                raise MediaAlreadyExists(f"{media_name} ({year})")
            else:
                transfer_film_to_jellyfin(
                    torrent_path=torrent_path,
                    jellyfin_film_path=FILM["folder"],
                    film_name=media_name,
                    year=year
                )
        elif chosen_media_type == TV_SHOW:
            season = read_tv_show_season()
            if is_tv_show_season_in_jellyfin(media_name, year, season):
                raise MediaAlreadyExists(
                    f"{media_name} ({year})/Season {str(season).zfill(2)}"
                )
            else:
                transfer_tv_show_season_to_jellyfin(
                    torrent_season_path=torrent_path,
                    jellyfin_tv_show_path=chosen_media_type["folder"],
                    tv_show=media_name,
                    year=year,
                    season=season
                )
        else:
            raise AssertionError("Invalid media type.")
        print_success("Media moved successfully.")
    except MediaAlreadyExists as e:
        print_error(f"Media '{e}' already exists.")
    except KeyboardInterrupt:
        print("\nExiting...")
        exit(1)


if __name__ == "__main__":
    main()
