import random
import string

# En simpel URL shortener der gemmer mappings mellem korte og lange URL'er i hukommelsen.
# den kan generere en kort kode for en given lang URL og kan også løse den korte kode tilbage til den lange URL.
class URLShortener:
    def __init__(self):
        self.url_map = {}


    # Genererer en tilfældig alfanumerisk streng af en given længde
    def _generate_short_code(self, length: int = 6) -> str:
        chars = string.ascii_letters + string.digits
        while True:
            code = ''.join(random.choice(chars) for _ in range(length))
            if code not in self.url_map:
                return code

    # Forkorter en lang URL og returnerer den korte kode
    def shorten(self, long_url: str) -> str:
                for code, url in self.url_map.items():
                    if url == long_url:
                        return code
            
                while True:
                    short_code = self._generate_short_code() 
                    if short_code not in self.url_map:
                        break

                self.url_map[short_code] = long_url
                return short_code

    # løser en kort kode til den originale lange URL
    def resolve(self, short_code: str) -> str:
        """
        Resolves a short code to its original long URL.
        Raises KeyError if the short code is not found.
        """
        if short_code not in self.url_map:
            raise KeyError(f"Short code '{short_code}' not found.")
        return self.url_map[short_code]

# nogle få manuelle tests
# for at sikre at shortener fungerer
if __name__ == '__main__':
    shortener = URLShortener()
    url1 = "https://www.example.com/very/long/path/to/document1"
    url2 = "https://www.another-example.net/another/long/path"

    code1 = shortener.shorten(url1)
    print(f"'{url1}' -> '{code1}'")

    code2 = shortener.shorten(url2)
    print(f"'{url2}' -> '{code2}'")

    # Test resolving
    print(f"Resolving '{code1}': {shortener.resolve(code1)}")

    # Test resolving again
    code1_again = shortener.shorten(url1)
    print(f"Shortening '{url1}' again: '{code1_again}' (should be same as '{code1}')")

    # Test resolving non-existent code
    try:
        shortener.resolve("invalid")
    except KeyError as e:
        print(e)