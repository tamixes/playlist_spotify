class ResponseException(Exception):
    def __init__(self, status_code, message):
        self.message = message
        self.status_code = status_code

    def __str__(self):
        return f"{self.status_code} - {self.message}"


class TrackNotFoundException(Exception):
    def __init__(self, song_name, artist):
        self.song_name = song_name
        self.artist = artist

    def __str__(self):
        return f"Track {self.song_name} of {self.artist} not found"
