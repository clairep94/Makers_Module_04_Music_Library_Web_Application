from lib.album import Album
# from album import Album
# from database_connection import DatabaseConnection

class AlbumRepository:

    # We initialise with a database connection
    def __init__(self, connection):
        self._connection = connection

    # Retrieve all albums
    def all(self):
        rows = self._connection.execute('SELECT albums.id AS album_id, albums.title, artists.name as artist_name, albums.release_year FROM artists JOIN albums ON albums.artist_id = artists.id')
        albums = []
        for row in rows:
            item = {"album_id": row["album_id"],
                    "title": row["title"],
                    "artist_name": row["artist_name"],
                    "release_year": row["release_year"]}
            albums.append(item)
        return albums
    

    # Check if album is a duplicate
    def is_duplicate(self, album_title, artist_id):
        album_title = album_title.title()

        rows = self._connection.execute('SELECT title, artist_id from albums')
        for row in rows:
            if album_title == row["title"] and artist_id == row["artist_id"]:
                return True
        return False    
    
    # Generate error for having duplicate album in database
    def generate_duplicate_error(self):
        return "Album is already in database"

    # Find a single album by their id
    def find(self, id):
        rows = self._connection.execute(
            'SELECT albums.id AS album_id, albums.title, artists.name as artist_name, albums.artist_id, albums.release_year FROM artists JOIN albums ON albums.artist_id = artists.id WHERE albums.id = %s', [id])
        row = rows[0]
        return {"album_id": row["album_id"],
                "title": row["title"],
                "artist_name": row["artist_name"],
                "artist_id": row["artist_id"],
                "release_year": row["release_year"]}

    # Create a new album
    # Do you want to get its id back? Look into RETURNING id;
    def create(self, album:Album):
        rows = self._connection.execute('INSERT INTO albums (title, release_year, artist_id) VALUES (%s, %s, %s) RETURNING id', [
            album.title, album.release_year, album.artist_id])
        row = rows[0]
        album.id = row['id']
        return album

    # Delete an album by their id
    def delete(self, id):
        self._connection.execute(
            'DELETE FROM albums WHERE id = %s', [id]
        )
        return None


    # Find artist id by artist name
    def find_artist_id_by_artist_name(self, artist_name):
        artist_name = artist_name.title()
        artist_row = self._connection.execute('SELECT id, name FROM artists WHERE name = %s', [artist_name])
        if artist_row == []:
            return None #Artist is not in the database.
        else:
            return artist_row[0]['id']
        
    # Generate error for not having artist in database
    def generate_add_artist_first_error(self):
        return "Artist for this album has not yet been added to the database. Please create new artist first."
