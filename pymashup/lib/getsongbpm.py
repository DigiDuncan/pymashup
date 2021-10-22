from dataclasses import dataclass
from typing import Literal, Optional
from urllib.parse import quote_plus
from functools import total_ordering

import cloudscraper

from pymashup import keys


s = cloudscraper.CloudScraper()
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

    @classmethod
    def from_json(cls, jsondata: dict):
        artist_id = jsondata["id"]
        name = jsondata["name"]
        uri = jsondata["uri"]
        img = jsondata["img"]
        genres = jsondata["genres"]
        origin = jsondata["from"]
        mbid = jsondata["mbid"]
        return Artist(artist_id, name, uri, img, genres, origin, mbid)


@dataclass(eq = False)
class Song:
    id: str
    title: str
    url: str
    artist: Artist
    tempo: Optional[float]
    time_sig: Optional[tuple[int, int]]
    key: Optional[tuple[KeyNum, bool]]

    def __lt__(self, other):
        if not isinstance(other, Song):
            raise ValueError(f"Song can only compare to Song, not {other.__class__.__name__}.")

        return self.tempo, self.key, self.title, self.id < self.tempo, self.key, self.title, self.id

    def __eq__(self, other):
        if not isinstance(other, Song):
            raise ValueError(f"Song can only compare to Song, not {other.__class__.__name__}.")

        return self.id == other.id

    @classmethod
    def from_json(cls, jsondata: dict):
        song_id = jsondata["id"]
        title = jsondata["title"]
        uri = jsondata["uri"]
        artist = Artist.from_json(jsondata["artist"])
        tempo = jsondata.get("tempo")
        time_sig = jsondata.get("time_sig")
        if time_sig is not None:
            time_sig = [int(i) for i in time_sig.split("/")]
        key_of = jsondata.get("key_of")
        if key_of is not None:
            key_of = str(key_of[:-1]), bool(key_of[-1])
        return Song(song_id, title, uri, artist, tempo, time_sig, key_of)


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
    response = s.get(f"https://api.getsongbpm.com/search/?type={mode}&lookup={lookup}")
    if response.status_code != 200:
        raise RuntimeError(f"Repsonse from GetSongBPM was code {response.status_code}. Reason: {response.reason}")
    return response.json()


def search_songs(song: str):
    lookup = quote_plus(song)
    songlist = _search("song", lookup)
    return [Song.from_json(j) for j in songlist["search"]]


def smart_search_songs(song: str):
    lookup = quote_plus(song)
    songlist = _search("song", lookup)
    id_list = [j["id"] for j in songlist["search"]]
    return [get_song(i) for i in id_list]


def search_artists(artist: str):
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
    response = s.get(f"https://api.getsongbpm.com/song/?id={song_id}")
    if response.status_code != 200:
        raise RuntimeError(f"Repsonse from GetSongBPM was code {response.status_code}. Reason: {response.reason}")
    j = response.json()
    return Song.from_json(j["song"])


def get_songs_near_tempo(tempo: int) -> list[Song]:
    pass


def get_songs_in_key(key: KeyNum, major: bool) -> list[Song]:
    pass
