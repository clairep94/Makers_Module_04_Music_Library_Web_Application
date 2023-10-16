from playwright.sync_api import Page, expect


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


#TODO
'''
If we create a new artist without a name or genre,
We see an error message
'''
def test_error_empty_artist(db_connection, page, test_web_address):
    db_connection.seed("seeds/music_library.sql")
    page.goto(f"http://{test_web_address}/artists/new")

    page.click("text=Create Artist")
    errors = page.locator(".t-errors")
    expect(errors).to_have_text("There were errors with your submission: Name can't be blank, Genre can't be blank")



#TODO
'''
When we try to Create a New Artist where there is an identical artist of the same name and genre,
We see an error message.
'''
def test_error_duplicate_artist(db_connection, page, test_web_address):
    db_connection.seed("seeds/music_library.sql")
    page.goto(f"http://{test_web_address}/artists/new")

    page.fill("input[name='name']", "Pixies")
    page.fill("input[name='genre']", "Rock")
    page.click("text=Create Artist")
    errors = page.locator(".t-errors")

    expect(errors).to_have_text("There were errors with your submission: Artist is already in database")


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


