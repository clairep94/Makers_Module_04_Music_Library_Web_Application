from playwright.sync_api import Page, expect

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
        "Back to All Albums",
        "Homepage"
    ])


#TODO
'''
When we go to Add a New Album
We should see a form to create a new album with a field for the name and a field for the genre.
If the album's artist already exists, we should be transported to the new page for the album created.
When we go to All Albums, we should see the new album added to the list of albums
When we go to the album's artist page, we should see the new album to the list of albums for that artist.

If the album's artist does not already exist, we should be notified, and provided a link to first create a new artist.
'''
def create_new_album(db_connection, page, test_web_address):
    db_connection.seed("seeds/music_library.sql")
    page.goto(f"http://{test_web_address}/albums/new")

    page.fill("input[name='title']", "Sunnbrella")
    page.fill("input[name='artist_name']", "Heartworn")
    page.fill("input[name='release_year']", 2023)
    page.click("text=Create Album")

    errors = page.locator(".t-errors")
    expect(errors).to_have_text("There were errors with your submission: Artist for this album has not yet been added to the database. Please create new artist first.")

    page.fill("input[name='title']", "pixies")
    page.fill("input[name='artist_name']", "trompe le monde")
    page.fill("input[name='release_year']", 1991)
    page.click("text=Create Album")

    title_element = page.locator(".t-title")
    expect(title_element).to_have_text("Title: Trompe Le Monde")
    release_year = page.locator(".t-release_year")
    expect(release_year).to_have_text("Release year: 1991")
    artist_name = page.locator(".t-artist_name")
    expect(artist_name).to_have_text("Artist: Pixies")


'''
If we create a new album without a title, artist or release year,
We see an error message
'''
def test_error_empty_album(db_connection, page, test_web_address):
    db_connection.seed("seeds/music_library.sql")
    page.goto(f"http://{test_web_address}/albums/new")

    page.click("text=Create Album")
    errors = page.locator(".t-errors")
    expect(errors).to_have_text("There were errors with your submission: Title can't be blank, Artist can't be blank, Release year can't be blank")

'''
If we create a new album that already exists (title, artist and release year are identical),
We see an error 
message
'''
def test_error_duplicate_album(db_connection, page, test_web_address):
    db_connection.seed("seeds/music_library.sql")
    page.goto(f"http://{test_web_address}/albums/new")

    page.fill("input[name='title']", "Doolittle")
    page.fill("input[name='artist_name']", "Pixies")
    page.fill("input[name='release_year']", '1989')

    page.click("text=Create Album")
    errors = page.locator(".t-errors")
    expect(errors).to_have_text("There were errors with your submission: Album is already in database")



'''
When we delete an album, we no longer see it in the albums index
'''
def test_delete_album(db_connection, page, test_web_address):
    db_connection.seed("seeds/music_library.sql")
    page.goto(f"http://{test_web_address}/albums/1")
    page.click("text=Delete Album")
    list_items = page.locator("li")
    expect(list_items).to_have_text([
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