import hashlib
from pydantic import BaseModel
from urlshortener.models import ShortenedURL, NotFound

class AlreadyExists(Exception):
    pass

class CreateShortenedURLCommand(BaseModel):
    url: str

    def execute(self) -> ShortenedURL:
        try:
            ShortenedURL.get_by_url(self.url)
            raise AlreadyExists
        except NotFound:
            pass

        short_url = Hash_url(self.url)
        # todo check for hash collisions
        shortened_url = ShortenedURL(url=self.url, short_url=short_url)
        shortened_url.save()

        return shortened_url

def Hash_url(url: str) -> str:
    """
    Hash the url to create a unique short url
    """
    enconded_url = url.encode('utf-8')
    return hashlib.sha256(enconded_url).hexdigest()[:6]