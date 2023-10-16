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
    


