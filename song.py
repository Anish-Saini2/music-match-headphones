"""
Song Class
Represents a song with Spotify audio features
"""


class Song:
    def __init__(self, track_id, track_name, track_artist, track_popularity,
                 playlist_genre, playlist_subgenre, danceability, energy,
                 valence, tempo, acousticness, loudness):
        """Initialize a Song object with Spotify audio features"""
        self.track_id = track_id
        self.track_name = track_name
        self.track_artist = track_artist
        self.track_popularity = int(track_popularity)
        self.playlist_genre = playlist_genre
        self.playlist_subgenre = playlist_subgenre
        self.danceability = float(danceability)
        self.energy = float(energy)
        self.valence = float(valence)
        self.tempo = float(tempo)
        self.acousticness = float(acousticness)
        self.loudness = float(loudness)

    def get_avg_energy(self):
        """Return the energy level of the song"""
        return self.energy

    def get_genre(self):
        """Return the genre of the song"""
        return self.playlist_genre

    def __str__(self):
        """String representation of the song"""
        return f"{self.track_name} by {self.track_artist} ({self.playlist_genre})"