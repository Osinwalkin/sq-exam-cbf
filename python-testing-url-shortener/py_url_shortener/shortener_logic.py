import random
import string

class URLShortener:
    def __init__(self):
        self.url_map = {}  # Stores short_code: long_url
        # Optional: a reverse map for quick checking if a long_url was already shortened
        # self.reverse_url_map = {} # Stores long_url: short_code

    def _generate_short_code(self, length: int = 6) -> str:
        """Generates a random alphanumeric string of a given length."""
        chars = string.ascii_letters + string.digits
        while True:
            code = ''.join(random.choice(chars) for _ in range(length))
            if code not in self.url_map: # Ensure uniqueness
                return code

    def shorten(self, long_url: str) -> str:
        """
        Shortens a long URL.
        If the URL has already been shortened, returns the existing short code.
        """
        # Optional: Check if long_url already exists (requires reverse_url_map or iterating values)
        # For simplicity on Day 1, we can skip this pre-check and always generate,
        # or add it if time permits. Let's assume for now we always generate if not directly found by code.
        # A more robust version would check if long_url is already a value in self.url_map.

        # Check if this exact long_url has already been shortened
        # This is a less efficient way if you don't have a reverse map
        for code, url in self.url_map.items():
            if url == long_url:
                return code
        
        short_code = self._generate_short_code()
        self.url_map[short_code] = long_url
        # if self.reverse_url_map: self.reverse_url_map[long_url] = short_code
        return short_code

    def resolve(self, short_code: str) -> str:
        """
        Resolves a short code to its original long URL.
        Raises KeyError if the short code is not found.
        """
        if short_code not in self.url_map:
            raise KeyError(f"Short code '{short_code}' not found.")
        return self.url_map[short_code]

if __name__ == '__main__': # Basic manual test
    shortener = URLShortener()
    url1 = "https://www.example.com/very/long/path/to/document1"
    url2 = "https://www.another-example.net/another/long/path"

    code1 = shortener.shorten(url1)
    print(f"'{url1}' -> '{code1}'")

    code2 = shortener.shorten(url2)
    print(f"'{url2}' -> '{code2}'")

    # Test resolving
    print(f"Resolving '{code1}': {shortener.resolve(code1)}")

    # Test shortening same URL again
    code1_again = shortener.shorten(url1)
    print(f"Shortening '{url1}' again: '{code1_again}' (should be same as '{code1}')")

    # Test resolving non-existent code
    try:
        shortener.resolve("invalid")
    except KeyError as e:
        print(e)