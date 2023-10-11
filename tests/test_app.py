from playwright.sync_api import Page, expect

# Tests for your routes go here

'''
When we go to the homepage,
We should get a link for All Albums and All Artists
'''
def test_home_page(db_connection, page, test_web_address):
    db_connection.seed("seeds/music_library.sql")
    page.goto(f"http://{test_web_address}/")
    header_two_items = page.locator("h2")




'''
We can get Album title, 
'''
def test_get_albums(db_connection, page, test_web_address):
    db_connection.seed("seeds/music_library.sql")
    page.goto(f"http://{test_web_address}/albums")
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
    
    
