from dataclasses import dataclass
from typing import Literal
from urllib.parse import quote_plus
from functools import total_ordering

import requests

from pymashup import keys


s = requests.Session()
s.params.update({'api_key': keys.getsongbpm})

Url = str
KeyNum = Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]


@total_ordering
@dataclass(eq = False)
class Artist:
    id: str
    name: str
    uri: Url
    img: Url
    genres: list[str]
    origin: str
    mbid: str

    def __lt__(self, other):
        if not isinstance(other, Artist):
            raise ValueError(f"Artist can only compare to Artist, not {other.__class__.__name__}.")

        return self.name, self.id < other.name, other.id

    def __eq__(self, other):
        if not isinstance(other, Artist):
            raise ValueError(f"Artist can only compare to Artist, not {other.__class__.__name__}.")

        return self.id == other.id


@dataclass(eq = False)
class Song:
    id: str
    title: str
    url: str
    artist: Artist
    tempo: float
    time_sig: tuple[int, int]
    key: tuple[KeyNum, bool]
    camelot: str

    def __lt__(self, other):
        if not isinstance(other, Song):
            raise ValueError(f"Song can only compare to Song, not {other.__class__.__name__}.")

        return self.tempo, self.key, self.title, self.id < self.tempo, self.key, self.title, self.id

    def __eq__(self, other):
        if not isinstance(other, Song):
            raise ValueError(f"Song can only compare to Song, not {other.__class__.__name__}.")

        return self.id == other.id


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
    response = s.get("https://api.getsongbpm.com/search", params = {"type": mode, "lookup": lookup})
    if response.status_code != 200:
        raise RuntimeError(f"Repsonse from GetSongBPM was code {response.status_code}. Reason: {response.reason}")
    return response.json()


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


def get_songs_in_key(key: KeyNum, major: bool) -> list[Song]:
    pass
