import os
from flask import Flask, request, render_template, redirect, url_for
from lib.database_connection import get_flask_database_connection

from lib.album import Album
from lib.album_repository import AlbumRepository
from lib.artist import Artist
from lib.artist_repository import ArtistRepository


# Create a new Flask app
app = Flask(__name__)

# == Your Routes Here ==

# == HOMEPAGE ==
@app.route('/', methods=['GET'])
def home_page():
    return render_template('homepage.html')


# == ALBUMS ==
# GET /albums
# Returns a list of albums
@app.route('/albums', methods=['GET'])
def get_albums():
    connection = get_flask_database_connection(app)
    album_repository = AlbumRepository(connection)
    albums = album_repository.all() #switched to list of dictionaries with artist_name included
    return render_template('albums/index.html', albums=albums)

# GET /albums/<id>
# Returns a single album
@app.route('/albums/<int:id>', methods=['GET'])
def get_album(id):
    connection = get_flask_database_connection(app)
    album_repository = AlbumRepository(connection)
    album = album_repository.find(id)
    return render_template('albums/show.html', album=album)

# GET /albums/new
# Returns a form to create a new album
@app.route('/albums/new', methods=['GET'])
def get_new_album_form():
    return render_template('albums/new.html')


# POST /albums
# Creates a new album - if the artist does not exist, it creates a new artist as well.
@app.route('/albums', methods=['POST'])
def create_new_album():
    connection = get_flask_database_connection(app)
    album_repository = AlbumRepository(connection)
    artist_repository = ArtistRepository(connection)
    title = request.form['title']
    artist_name = request.form['artist_name'] #TEST THIS AFTER
    release_year = request.form['release_year']
    print(f"Title:{title}")
    print(f"Artist:{artist_name}")
    print(f"Release Year: {release_year}")    

    # FIND ARTIST_ID FOR ARTIST.
    # If no artist_name found, create new_artist() AND
    # create new_album()





# == ARTISTS ==

@app.route('/artists/<int:id>', methods=['GET'])
def get_artist(id):
    connection = get_flask_database_connection(app)
    artist_repository = ArtistRepository(connection)
    artist = artist_repository.find(id)
    artist_albums = artist_repository.find_all_albums_by_artist(id)
    return render_template('artists/show.html', artist=artist, albums=artist_albums)

@app.route('/artists', methods=['GET'])
def get_artists():
    connection = get_flask_database_connection(app)
    artist_repository = ArtistRepository(connection)
    artists = artist_repository.all()
    return render_template('artists/index.html', artists=artists)


# GET /artists/new
# Returns a form to create a new artist
@app.route('/artists/new', methods=['GET'])
def get_new_artist_form():
    return render_template('artists/new.html')


# POST /artist
# Creates a new artist
@app.route('/artists', methods=['POST'])
def create_new_artist():
    connection = get_flask_database_connection(app)
    print("DB connection created")
    artist_repository = ArtistRepository(connection)
    print("Artist repository connection created")

    print("Testing request.form")
    print(f"Form Data: {request.form}")
    name = request.form.get('name')
    print(f"Artist:{name}")
    genre = request.form.get('genre') 
    print(f"Genre:{genre}")


    artist = Artist(None, name, genre)
    print(f"Artist successfully created: {artist}")
    # if not artist.is_valid():
        #return render_template('artists/new.html', artist=artist, errors=artist.generate_errors()), 400
    # if not artist_repository.is_valid():
        #return render_template('artists/new.html', artist=artist, errors=artist.generate_errors()), 400


    artist = artist_repository.create(artist) #no longer returning none.
    print(f"Artist successfully created: {artist}")
    return redirect(f"/artists/{artist.id}")






# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
