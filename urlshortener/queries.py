from typing import List
from pydantic import BaseModel
from urlshortener.models import ShortenedURL

class ListShortenedURLsQuery(BaseModel):
    def execute(self) -> List[ShortenedURL]:
        return ShortenedURL.list()

class GetShortenedURLByIdQuery(BaseModel):
    id: str

    def execute(self) -> ShortenedURL:
        return ShortenedURL.get_by_id(self.id)

class GetShortenedURLByShortURLQuery(BaseModel):
    short_url: str

    def execute(self) -> ShortenedURL:
        return ShortenedURL.get_by_short_url(self.short_url)

class GetShortenedURLByURLQuery(BaseModel):
    url: str

    def execute(self) -> ShortenedURL:
        return ShortenedURL.get_by_url(self.url)