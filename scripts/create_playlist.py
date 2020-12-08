import requests

import json
import logging

from .exceptions import ResponseException, TrackNotFoundException
from .musics import musics_tuple
from .utils import (CREATE_PLAYLIST_URL,
                    HEADERS,
                    SEARCH_MUSIC_URL,
                    PLAYLIST_URL,
                    PLAYLIST_DATA)

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class SpotifyPlaylist:

    def search_spotify_music(self, song_name, artist):
        """Searchs the song.
        """
        search_request = requests.get(
            SEARCH_MUSIC_URL(song=song_name, artist=artist),
            headers=HEADERS,
        )

        logger.info('Searching for song %s by artist %s.', song_name, artist)

        response = search_request.json()
        self._check_error_status(response)

        tracks = response.get('tracks')

        self._check_search_result(tracks, song_name, artist)
        songs = tracks["items"]
        uri = songs[0]["uri"]

        return uri

    def creates_playlist(self):
        """Creates the new playlist.
        """

        playlist_request = requests.post(
            CREATE_PLAYLIST_URL,
            data=PLAYLIST_DATA,
            headers=HEADERS,
        )

        created_playlist_response = playlist_request.json()

        return created_playlist_response["id"]

    def add_song_to_playlist(self):
        """Adds the songs to the new playlist.
        """
        uris = [self.search_spotify_music(m[0], m[1]) for m in musics_tuple]

        playlist_id = self.creates_playlist()

        request_data = json.dumps(uris)

        add_song_request = requests.post(
            PLAYLIST_URL(playlist_id),
            data=request_data,
            headers=HEADERS,
        )
        response = add_song_request.json()

        self._check_error_status(response)
        logger.info('(%d) songs adds to the new playlist.' % len(uris))
        return response

    def _check_error_status(self, response):
        """Checks if the response has return any error.
        """

        if response.get("error"):
            message = response['error']['message']
            status = response['error']['status']
            raise ResponseException(status, message)

    def _check_search_result(self, tracks, song_name, artist):
        """Checks if the search has return any song.
        """

        result = tracks.get('total')
        if result == 0:
            raise TrackNotFoundException(song_name, artist)
