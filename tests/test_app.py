from playwright.sync_api import Page, expect

# Tests for your routes go here

# === HOMEPAGE === #
'''
When we go to the homepage,
We should get a link for All Albums and All Artists
'''
def test_home_page(db_connection, page, test_web_address):
    db_connection.seed("seeds/music_library.sql")
    page.goto(f"http://{test_web_address}/")
    header_one_items = page.locator("h1")
    expect(header_one_items).to_have_text("Music Library HTML Project")
    anchor_tags = page.locator("a")
    expect(anchor_tags).to_have_text([
        "All Artists",
        "All Albums"
    ])
    expect(page.get_by_text("All Artists")).to_have_attribute("href", "/artists")
    expect(page.get_by_text("All Albums")).to_have_attribute("href", "/albums")
    


# === ARTISTS ==== #

'''
When we go to artists,
We should get a list of all artists on our database.
We should be able to click on each artist to get to their artist page
We should be able to click on a link to Add a New Artist
We should be able to go back to the homepage.
'''    
def test_get_artists(db_connection, page, test_web_address):
    db_connection.seed("seeds/music_library.sql")
    page.goto(f"http://{test_web_address}/artists")
    header_one_items = page.locator("h1")
    expect(header_one_items).to_have_text("All Artists")
    list_items = page.locator("li")
    expect(list_items).to_have_text([
        "Pixies, Rock",
        "ABBA, Pop",
        "Taylor Swift, Pop",
        "Nina Simone, Jazz"
    ])

    anchor_tags = page.locator("a")
    expect(anchor_tags).to_have_text([
        "Pixies",
        "ABBA",
        "Taylor Swift",
        "Nina Simone",
        "Add a New Artist",
        "Homepage"
    ])
    expect(page.get_by_text("Pixies")).to_have_attribute("href", "/artists/1")
    expect(page.get_by_text("ABBA")).to_have_attribute("href", "/artists/2")
    expect(page.get_by_text("Taylor Swift")).to_have_attribute("href", "/artists/3")
    expect(page.get_by_text("Nina Simone")).to_have_attribute("href", "/artists/4")
    expect(page.get_by_text("Add a New Artist")).to_have_attribute("href", "/artists/new")
    expect(page.get_by_text("Homepage")).to_have_attribute("href", "/")


    
'''
When we go to the page for a single artist
We should see the artist name and a list of all their albums, with links to the album pages.
We should see a link to delete the artist
'''
def test_get_artist(db_connection, page, test_web_address):
    db_connection.seed("seeds/music_library.sql")
    page.goto(f"http://{test_web_address}/artists/1")
    header_one_items = page.locator("h1")
    expect(header_one_items).to_have_text("Pixies")
    paragraph_items = page.locator("p")
    expect(paragraph_items).to_have_text([
        "Name: Pixies",
        "Genre: Rock",
        "Albums: "
        ])
    
    list_items = page.locator("li")
    expect(list_items).to_have_text([
        "Doolittle (1989)",
        "Surfer Rosa (1988)",
        "Bossanova (1990)"
    ])

    expect(page.get_by_text("Doolittle (1989)")).to_have_attribute("href", "/albums/1")
    expect(page.get_by_text("Surfer Rosa (1988)")).to_have_attribute("href", "/albums/2")
    expect(page.get_by_text("Bossanova (1990)")).to_have_attribute("href", "/albums/5")
    expect(page.get_by_text("Homepage")).to_have_attribute("href", "/")

    expect(page.locator('button:has-text("Delete Artist")')) != None #button with Delete Artist exists


'''
When we go to Add a New Artist
We should see a form to create a new artist with a field for Name and a field for Genre.
When we click Create Artist, we should be linked to the artist page for the new artist.
When we click Back to All Artists, we should see that the new artist has been added to all artists
'''
def test_create_artist(db_connection, page, test_web_address):
    db_connection.seed("seeds/music_library.sql")
    page.goto(f"http://{test_web_address}/artists/new")
    header_one_items = page.locator("h1")
    expect(header_one_items).to_have_text("Add a New Artist")

    page.fill("input[name='name']", "The Beatles")
    page.fill("input[name='genre']", "Pop")
    page.click("text=Create Artist")

    title_element = page.locator(".t-name")
    expect(title_element).to_have_text("Name: The Beatles")

    author_element = page.locator(".t-genre")
    expect(author_element).to_have_text("Genre: Pop")

    page.click("text=Back to All Artists")
    list_items = page.locator("li")
    expect(list_items).to_have_text([
        "Pixies, Rock",
        "ABBA, Pop",
        "Taylor Swift, Pop",
        "Nina Simone, Jazz",
        "The Beatles, Pop"
    ])
    expect(page.get_by_text("The Beatles")).to_have_attribute("href", "/artists/5")



'''
If we create a new artist without a name or genre,
We see an error message

'''

'''
When we try to Create a New Artist where there is an identical artist of the same name and genre,
We see an error message.
'''


'''
When we delete an artist, we no longer see it in the artists index
'''
def test_delete_artist(db_connection, page, test_web_address):
    db_connection.seed("seeds/music_library.sql")
    page.goto(f"http://{test_web_address}/artists/new")

    page.fill("input[name='name']", "The Beatles")
    page.fill("input[name='genre']", "Pop")
    page.click("text=Create Artist")

    page.click("text=Delete Artist")
    list_items = page.locator("li")
    expect(list_items).to_have_text([
        "Pixies, Rock",
        "ABBA, Pop",
        "Taylor Swift, Pop",
        "Nina Simone, Jazz"
    ])

'''
When we delete an artist, we no longer see its albums in all albums
'''
def test_delete_artist2(db_connection, page, test_web_address):
    db_connection.seed("seeds/music_library.sql")
    page.goto(f"http://{test_web_address}/artists/1")

    page.click("text=Delete Artist")
    list_items = page.locator("li")
    expect(list_items).to_have_text([
        "ABBA, Pop",
        "Taylor Swift, Pop",
        "Nina Simone, Jazz"
    ])

    page.goto(f"http://{test_web_address}/albums")
    list_items = page.locator("li")
    expect(list_items).to_have_text([
        "Waterloo (1974) by ABBA",
        "Super Trouper (1980) by ABBA",
        "Lover (2019) by Taylor Swift",
        "Folklore (2020) by Taylor Swift",
        "I Put a Spell on You (1965) by Nina Simone",
        "Baltimore (1978) by Nina Simone",
        "Here Comes the Sun (1971) by Nina Simone",
        "Fodder on My Wings (1982) by Nina Simone",
        "Ring Ring (1973) by ABBA"
    ])


# === ALBUMS ==== #

'''
When we go to albums,
We should get a list of all albums on our database.
We should be able to click on each album to get to its album page
We should be able to click on a link to Add a New Album
We should be able to go back to the homepage.
'''
def test_get_albums(db_connection, page, test_web_address):
    db_connection.seed("seeds/music_library.sql")
    page.goto(f"http://{test_web_address}/albums")
    header_one_items = page.locator("h1")
    expect(header_one_items).to_have_text("All Albums")
    list_items = page.locator("li")
    expect(list_items).to_have_text([
        "Doolittle (1989) by Pixies",
        "Surfer Rosa (1988) by Pixies",
        "Waterloo (1974) by ABBA",
        "Super Trouper (1980) by ABBA",
        "Bossanova (1990) by Pixies",
        "Lover (2019) by Taylor Swift",
        "Folklore (2020) by Taylor Swift",
        "I Put a Spell on You (1965) by Nina Simone",
        "Baltimore (1978) by Nina Simone",
        "Here Comes the Sun (1971) by Nina Simone",
        "Fodder on My Wings (1982) by Nina Simone",
        "Ring Ring (1973) by ABBA"
    ])
    anchor_tags = page.locator("a")
    expect(anchor_tags).to_have_text([
        "Doolittle (1989)",
        "Surfer Rosa (1988)",
        "Waterloo (1974)",
        "Super Trouper (1980)",
        "Bossanova (1990)",
        "Lover (2019)",
        "Folklore (2020)",
        "I Put a Spell on You (1965)",
        "Baltimore (1978)",
        "Here Comes the Sun (1971)",
        "Fodder on My Wings (1982)",
        "Ring Ring (1973)",
        "Add a New Album",
        "Homepage"
    ])
    expect(page.get_by_text("Doolittle (1989)")).to_have_attribute("href", "/albums/1")
    expect(page.get_by_text("Surfer Rosa (1988)")).to_have_attribute("href", "/albums/2")
    expect(page.get_by_text("Waterloo (1974)")).to_have_attribute("href", "/albums/3")
    expect(page.get_by_text("Super Trouper (1980)")).to_have_attribute("href", "/albums/4")
    expect(page.get_by_text("Bossanova (1990)")).to_have_attribute("href", "/albums/5")
    expect(page.get_by_text("Lover (2019)")).to_have_attribute("href", "/albums/6")
    expect(page.get_by_text("Folklore (2020)")).to_have_attribute("href", "/albums/7")
    expect(page.get_by_text("I Put a Spell on You (1965)")).to_have_attribute("href", "/albums/8")
    expect(page.get_by_text("Baltimore (1978)")).to_have_attribute("href", "/albums/9")
    expect(page.get_by_text("Here Comes the Sun (1971)")).to_have_attribute("href", "/albums/10")
    expect(page.get_by_text("Fodder on My Wings (1982)")).to_have_attribute("href", "/albums/11")
    expect(page.get_by_text("Ring Ring (1973)")).to_have_attribute("href", "/albums/12")
    expect(page.get_by_text("Add a New Album")).to_have_attribute("href", "/albums/new")
    expect(page.get_by_text("Homepage")).to_have_attribute("href", "/")


'''
When we go to an album
We expect to see its title, release year and artist
We expect to link to the artist page, all albums and the home page.
We expect a button to be able to delete the album.
'''

def test_get_album(db_connection, page, test_web_address):
    db_connection.seed("seeds/music_library.sql")
    page.goto(f"http://{test_web_address}/albums")
    page.click("text=Doolittle")
    title_element = page.locator(".t-title")
    expect(title_element).to_have_text("Title: Doolittle")
    release_year = page.locator(".t-release_year")
    expect(release_year).to_have_text("Release year: 1989")
    artist_name = page.locator(".t-artist_name")
    expect(artist_name).to_have_text("Artist: Pixies")
    
    expect(page.get_by_text("Pixies")).to_have_attribute("href", "/artists/1")
    expect(page.get_by_text("Back to All Albums")).to_have_attribute("href", "/albums")
    expect(page.get_by_text("Homepage")).to_have_attribute("href", "/")



    anchor_tags = page.locator("a")
    expect(anchor_tags).to_have_text([
        "Pixies",
        "Back to all albums",
        "Homepage"
    ])



'''
When we go to Add a New Album
We should see a form to create a new album with a field for the name and a field for the genre.
If the album's artist already exists, we should be transported to the new page for the album created.
When we go to All Albums, we should see the new album added to the list of albums
When we go to the album's artist page, we should see the new album to the list of albums for that artist.

If the album's artist does not already exist, we should be notified, and provided a link to first create a new artist.
'''


'''
If we create a new album without a name, artist or release year,
We see an error message
'''


'''
When we delete an album, we no longer see it in the albums index
'''


'''
When we try to Create a New Album where there is an identical album of the same name, artist, and release year,
We see an error message.
'''