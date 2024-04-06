import datetime
import os

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


def setup_film_data():
    torrent_name = "The.Lion.King.2019.x264.720p"
    film_folder = os.path.join(TORRENTS_PATH, torrent_name)
    os.makedirs(film_folder)
    base_file_path = os.path.join(film_folder, torrent_name)
    video_path = base_file_path + ".mkv"
    subtitle_path = base_file_path + ".srt"
    open(video_path, "w").close()
    open(subtitle_path, "w").close()
    return film_folder


def setup_tv_show_season_data():
    torrent_name = "Modern.Family.2010.x264.Season.5"
    tv_show_folder = os.path.join(TORRENTS_PATH, torrent_name)
    os.makedirs(tv_show_folder)
    season_folder = os.path.join(tv_show_folder, "season-5")
    os.makedirs(season_folder)
    base_file_path = os.path.join(season_folder, "Modern Family Episode ")
    video1_path = base_file_path + "1 S05E01 x264.mkv"
    subtitle1_path = base_file_path + "1 S05E01 x264.srt"
    video2_path = base_file_path + "2 S05E02 x264.mkv"
    subtitle2_path = base_file_path + "2 S05E02 x264.srt"
    open(video1_path, "w").close()
    open(subtitle1_path, "w").close()
    open(video2_path, "w").close()
    open(subtitle2_path, "w").close()
    return season_folder


def test_transfer_film_folder():
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


def test_transfer_tv_show_season_folder():
    tv_show_season_folder = setup_tv_show_season_data()
    
    transfer_tv_show_season_to_jellyfin(
        torrent_season_path=tv_show_season_folder,
        jellyfin_tv_show_path=TV_SHOW_FOLDER,
        tv_show="Modern Family",
        year=2010,
        season=5
    )
    
    assert not os.path.exists(tv_show_season_folder)
    jellyfin_tv_show_folder = os.path.join(
        TV_SHOW_FOLDER, "Modern Family (2010)", "Season 05"
    )
    assert os.path.exists(jellyfin_tv_show_folder)
    assert os.path.exists(
        os.path.join(jellyfin_tv_show_folder, f"Modern Family S05E01.mkv")
    )
    assert os.path.exists(
        os.path.join(jellyfin_tv_show_folder, f"Modern Family S05E02.srt")
    )


if __name__ == '__main__':
    unittest.main()
