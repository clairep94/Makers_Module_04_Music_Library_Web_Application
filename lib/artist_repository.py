from lib.artist import Artist

class ArtistRepository:

    # We initialise with a database connection
    def __init__(self, connection):
        self._connection = connection

    # Retrieve all artists
    def all(self):
        rows = self._connection.execute('SELECT * from artists')
        artists = []
        for row in rows:
            item = Artist(row["id"], row["name"], row["genre"])
            artists.append(item)
        return artists

    # Check if the name and genre of the new artist already exists in the repository.
    def is_duplicate(self, name, genre):
        name = name.title()
        genre = genre.title()
        rows = self._connection.execute('SELECT name, genre from artists')

        is_duplicate = False

        new_artist = (name, genre)
        for row in rows:
            artist = (row["name"], row["genre"])
            if new_artist == artist:
                is_duplicate = True
        return is_duplicate

    # Generate errors if the artist about to be created is a duplicate.
    def generate_errors(self):
        return "Artist is already in database"

    # Find a single artist by their id
    def find(self, artist_id):
        rows = self._connection.execute(
            'SELECT * from artists WHERE id = %s', [artist_id])
        row = rows[0]
        return Artist(row["id"], row["name"], row["genre"])

    # Create a new artist
    # Do you want to get its id back? Look into RETURNING id;
    def create(self, artist:Artist):
        rows = self._connection.execute('INSERT INTO artists (name, genre) VALUES (%s, %s) RETURNING id', [
            artist.name, artist.genre])
        row = rows[0]
        artist.id = row['id']
        return artist

    # Delete an artist by their id
    def delete(self, artist_id):
        self._connection.execute(
            'DELETE FROM artists WHERE id = %s', [artist_id])
        return None
    
    # Find all albums by a certain artist
    def find_all_albums_by_artist(self, artist_id):
        rows = self._connection.execute('SELECT title, release_year, id FROM albums WHERE artist_id = %s', [artist_id])
        albums = []
        for row in rows:
            album = {'title' : row["title"], 'release_year': row["release_year"], 'id': row["id"]}
            albums.append(album)
        return albums
