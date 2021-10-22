from dataclasses import dataclass
from typing import Literal
from urllib.parse import quote_plus

import requests

from pymashup import keys


s = requests.Session()
s.headers.update({'x-api-key': keys.getsongbpm})

Url = str


@dataclass
class Artist:
    id: str
    name: str
    uri: Url
    img: Url
    genres: list[str]
    origin: str
    mbid: str


@dataclass
class Song:
    id: str
    title: str
    url: str
    artist: Artist
    tempo: float
    time_sig: tuple[int, int]
    key: str
    camelot: str


@dataclass
class Tempo:
    song_id: str
    song_title: str
    song_uri: str
    tempo: float
    artist: Artist
    album: dict  # ???


@dataclass
class Key:
    song_id: str
    song_title: str
    song_uri: Url
    music_key: dict[str, str]
    artist: Artist
    album: dict  # ???


def _search(mode: Literal["song", "artist", "both"], lookup: str):
    pass


def search_song(song: str):
    lookup = quote_plus(song)
    return _search("song", lookup)


def search_artist(artist: str):
    lookup = quote_plus(artist)
    return _search("artist", lookup)


def search_song_and_artist(song: str, artist: str):
    song = quote_plus(song)
    artist = quote_plus(artist)
    lookup = f"song:{song} artist:{artist}"
    return _search("both", lookup)


def get_artist(artist_id: str) -> Artist:
    pass


def get_song(song_id: str) -> Song:
    pass


def get_songs_near_tempo(tempo: int) -> list[Song]:
    pass


def get_songs_in_key(key: int, mode: Literal[0, 1]) -> list[Song]:
    pass
