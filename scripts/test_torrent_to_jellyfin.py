import datetime
import os
import shutil
from pathlib import Path

import pytest
import unittest

from torrent_to_jellyfin import transfer_film_to_jellyfin, \
    transfer_tv_show_season_to_jellyfin

RUN_ID = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

TORRENTS_PATH = os.path.expanduser(f"tmp/{RUN_ID}/Torrents")
JELLYFIN_PATH = os.path.expanduser(f"tmp/{RUN_ID}/Jellyfin")
FILM_FOLDER = os.path.join(JELLYFIN_PATH, "Films")
TV_SHOW_FOLDER = os.path.join(JELLYFIN_PATH, "TV Shows")


@pytest.fixture
def setup_folder_structure():
    os.makedirs(TORRENTS_PATH, exist_ok=True)
    os.makedirs(JELLYFIN_PATH, exist_ok=True)
    os.makedirs(
        os.path.join(JELLYFIN_PATH, "Films"), exist_ok=True
    )
    os.makedirs(
        os.path.join(JELLYFIN_PATH, "TV Shows"), exist_ok=True
    )
    yield


# TV_SHOW_TORRENT_NAME = "Modern.Family.2010.x264.Season.5"


def setup_film_data():
    torrent_name = "The.Lion.King.2019.x264.720p"
    film_folder = os.path.join(TORRENTS_PATH, torrent_name)
    os.makedirs(film_folder, exist_ok=True)
    base_file_path = os.path.join(film_folder, torrent_name)
    film_path = base_file_path + ".mkv"
    subtitle_path = base_file_path + ".srt"
    open(film_path, "w").close()
    open(subtitle_path, "w").close()
    return film_folder


def test_move_film_folder():
    film_folder = setup_film_data()
    
    transfer_film_to_jellyfin(
        torrent_path=film_folder,
        jellyfin_film_path=FILM_FOLDER,
        film_name="The Lion King",
        year=2019
    )
    
    assert not os.path.exists(film_folder)
    jellyfin_film_folder = os.path.join(FILM_FOLDER, "The Lion King (2019)")
    assert os.path.exists(jellyfin_film_folder)
    assert os.path.exists(
        os.path.join(jellyfin_film_folder, "The Lion King.mkv")
    )
    assert os.path.exists(
        os.path.join(jellyfin_film_folder, "The Lion King.srt")
    )


if __name__ == '__main__':
    unittest.main()
