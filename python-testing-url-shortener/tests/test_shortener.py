import pytest
from py_url_shortener.shortener_logic import URLShortener

#Disse er unit tests til URLShortener class.
@pytest.fixture
# ny instans af URLShortener klassen
def shortener_instance():
    return URLShortener()

# Tester om shorten metoden fungerer korrekt
def test_shorten_creates_valid_short_code(shortener_instance):
    long_url = "https://www.example.com/path/to/something"
    short_code = shortener_instance.shorten(long_url)
    assert isinstance(short_code, str)
    assert len(short_code) == 6  # Assuming default length
    assert short_code in shortener_instance.url_map

# Tester om resolve metoden returnerer den korrekte lange URL
def test_resolve_returns_original_url(shortener_instance):
    long_url = "https://www.google.com/search?q=pytest"
    short_code = shortener_instance.shorten(long_url)
    resolved_url = shortener_instance.resolve(short_code)
    assert resolved_url == long_url

# Tester om resolve metoden kaster en KeyError hvis koden ikke findes
def test_resolve_unknown_code_raises_keyerror(shortener_instance):
    with pytest.raises(KeyError) as excinfo:
        shortener_instance.resolve("nonexistentcode")
    assert "not found" in str(excinfo.value).lower()

# tester om shorten metoden returnerer den samme kode for den samme URL
def test_shorten_same_url_returns_same_code(shortener_instance):
    long_url = "https://www.myuniqueurl.com/page"
    code1 = shortener_instance.shorten(long_url)
    code2 = shortener_instance.shorten(long_url)
    assert code1 == code2

# tester om shorten metoden returnerer forskellige koder for forskellige URL'er
def test_shorten_different_urls_returns_different_codes(shortener_instance):
    url1 = "https://site1.com"
    url2 = "https://site2.com"
    code1 = shortener_instance.shorten(url1)
    code2 = shortener_instance.shorten(url2)
    assert code1 != code2
    assert shortener_instance.resolve(code1) == url1
    assert shortener_instance.resolve(code2) == url2


#parametrize bliver brugt til at køre testen med forskellige URL'er
# Eksempel på at teste shorten med forskellige gyldige URL'er
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

# Eksempel på at teste shorten med forskellige problematiske inputs
# (eller inputs, der *burde* forårsage en fejl, hvis du tilføjede validering)
@pytest.mark.parametrize("edge_case_url", [
    "",  # Empty string
    "a", # Very short string
    " " * 1000, # Very long string of spaces
    "just-a-string-no-protocol",
])
def test_shorten_edge_case_inputs(shortener_instance, edge_case_url):
    short_code = shortener_instance.shorten(edge_case_url)
    assert isinstance(short_code, str)
    assert len(short_code) == 6
    assert shortener_instance.resolve(short_code) == edge_case_url


# Eksempel på at teste resolve med forskellige gyldige koder
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

# Kombination af shorten og resolve
# Test at forkorte en URL og derefter løse den
@pytest.mark.parametrize("url_to_shorten_and_resolve", [
    "https://www.paramtest1.com",
    "http://paramtest2.org/path",
])
def test_shorten_and_resolve_cycle_parametrized(shortener_instance, url_to_shorten_and_resolve):
    short_code = shortener_instance.shorten(url_to_shorten_and_resolve)
    resolved_url = shortener_instance.resolve(short_code)
    assert resolved_url == url_to_shorten_and_resolve


# Test shorten ved at kontrollere at den genererede kode ikke allerede findes
# Dette er for at mocke _generate_short_code metoden
def test_shorten_uses_generated_code(shortener_instance, mocker):
    long_url = "https://www.specific-url.com"
    expected_short_code = "mocked"

    mocker.patch.object(shortener_instance, '_generate_short_code', return_value=expected_short_code)

    actual_short_code = shortener_instance.shorten(long_url)

    assert actual_short_code == expected_short_code

    shortener_instance._generate_short_code.assert_called_once()

    assert shortener_instance.url_map[expected_short_code] == long_url

# Test at forkorte en URL, der allerede er forkortet
# og kontrollere at den returnerer den samme kode
def test_shorten_retries_if_generated_code_collides(shortener_instance, mocker):
    long_url1 = "https://url1.com"
    long_url2 = "https://url2.com"
    colliding_code = "collide"
    unique_code = "unique"

    shortener_instance.url_map[colliding_code] = long_url1 

    mock_generator = mocker.patch.object(shortener_instance, '_generate_short_code')
    mock_generator.side_effect = [colliding_code, unique_code]


    actual_short_code_for_url2 = shortener_instance.shorten(long_url2)

    assert actual_short_code_for_url2 == unique_code
    assert mock_generator.call_count == 2
    assert shortener_instance.url_map[unique_code] == long_url2