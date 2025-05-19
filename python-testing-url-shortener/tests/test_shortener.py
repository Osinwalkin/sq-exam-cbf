import pytest
from py_url_shortener.shortener_logic import URLShortener

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