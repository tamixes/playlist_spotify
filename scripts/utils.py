import json

from .info import (spotify_token,
                   spotify_id,
                   playlist_description,
                   playlist_name)

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer {token}".format(token=spotify_token)
}

PLAYLIST_DATA = json.dumps({
    "name": "{name}".format(name=playlist_name),
    "description": "{description}".format(description=playlist_description),
    "public": True
})

SEARCH_MUSIC_URL = ("https://api.spotify.com/v1/search?query=track%3A{song}+"
                    "artist%3A{artist}&type=track&offset=0&limit=20".format)

CREATE_PLAYLIST_URL = ("https://api.spotify.com/v1/users/{id}/playlists"
                       .format(id=spotify_id))

PLAYLIST_URL = "https://api.spotify.com/v1/playlists/{}/tracks".format
