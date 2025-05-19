import pytest
from py_url_shortener.shortener_logic import URLShortener

#These are the unit tests for the URLShortener class
@pytest.fixture
def shortener_instance():
    """Provides a fresh URLShortener instance for each test."""
    return URLShortener()

def test_shorten_creates_valid_short_code(shortener_instance):
    long_url = "https://www.example.com/path/to/something"
    short_code = shortener_instance.shorten(long_url)
    assert isinstance(short_code, str)
    assert len(short_code) == 6  # Assuming default length
    assert short_code in shortener_instance.url_map

def test_resolve_returns_original_url(shortener_instance):
    long_url = "https://www.google.com/search?q=pytest"
    short_code = shortener_instance.shorten(long_url)
    resolved_url = shortener_instance.resolve(short_code)
    assert resolved_url == long_url

def test_resolve_unknown_code_raises_keyerror(shortener_instance):
    with pytest.raises(KeyError) as excinfo:
        shortener_instance.resolve("nonexistentcode")
    assert "not found" in str(excinfo.value).lower() # Check part of the error message

def test_shorten_same_url_returns_same_code(shortener_instance):
    long_url = "https://www.myuniqueurl.com/page"
    code1 = shortener_instance.shorten(long_url)
    code2 = shortener_instance.shorten(long_url)
    assert code1 == code2

def test_shorten_different_urls_returns_different_codes(shortener_instance):
    url1 = "https://site1.com"
    url2 = "https://site2.com"
    code1 = shortener_instance.shorten(url1)
    code2 = shortener_instance.shorten(url2)
    assert code1 != code2
    assert shortener_instance.resolve(code1) == url1
    assert shortener_instance.resolve(code2) == url2




#parametrize is used to run the same test with different inputs
# Example for testing various valid URLs
@pytest.mark.parametrize("long_url_input", [
    "https://www.example.com",
    "http://subdomain.example.org/path?query=123",
    "https://anotherexample.net/a/b/c/d/e/f/g/h/i/j/k/l/m/n/o/p",
    "http://example.com:8080/path",
])
def test_shorten_various_valid_urls(shortener_instance, long_url_input):
    short_code = shortener_instance.shorten(long_url_input)
    assert isinstance(short_code, str)
    assert len(short_code) == 6 # Or whatever your defined length is
    assert shortener_instance.resolve(short_code) == long_url_input

# Example for testing how shorten handles potentially problematic inputs
# (or inputs that *should* cause an error if you added validation)
# This example assumes no strict input validation in `shorten` itself yet,
# so it just checks that it produces a short code.
# If you add validation that raises an error, you'd change this test.
@pytest.mark.parametrize("edge_case_url", [
    "",  # Empty string
    "a", # Very short string
    " " * 1000, # Very long string of spaces
    "just-a-string-no-protocol",
])
def test_shorten_edge_case_inputs(shortener_instance, edge_case_url):
    # Assuming for now that any string can be "shortened" without error
    # If you add validation to raise errors for these, adjust the test
    short_code = shortener_instance.shorten(edge_case_url)
    assert isinstance(short_code, str)
    assert len(short_code) == 6
    assert shortener_instance.resolve(short_code) == edge_case_url




# Example for testing resolve with various non-existent codes
# added more tests 
@pytest.mark.parametrize("invalid_code, expected_exception_message_part", [
    ("INVALID", "not found"),
    ("", "not found"), # Assuming empty string is an invalid code
    ("1234567", "not found"), # Potentially too long, or just non-existent
    ("שコード", "not found"), # Non-alphanumeric if your codes are restricted
])
def test_resolve_various_invalid_codes_raises_keyerror(shortener_instance, invalid_code, expected_exception_message_part):
    with pytest.raises(KeyError) as excinfo:
        shortener_instance.resolve(invalid_code)
    assert expected_exception_message_part.lower() in str(excinfo.value).lower()

# You can also combine `shorten` and `resolve` in a parametrized test
@pytest.mark.parametrize("url_to_shorten_and_resolve", [
    "https://www.paramtest1.com",
    "http://paramtest2.org/path",
])
def test_shorten_and_resolve_cycle_parametrized(shortener_instance, url_to_shorten_and_resolve):
    short_code = shortener_instance.shorten(url_to_shorten_and_resolve)
    resolved_url = shortener_instance.resolve(short_code)
    assert resolved_url == url_to_shorten_and_resolve