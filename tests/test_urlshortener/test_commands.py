import pytest

from urlshortener.models import ShortenedURL
from urlshortener.commands import CreateShortenedURLCommand, AlreadyExists

def test_create_shortened_url():
    """
    GIVEN a CreateShortenedURL command with valid URL
    WHEN the command is executed
    THEN a new ShortenedURL is created
    """

    cmd = CreateShortenedURLCommand(url='http://example.com')

    shortened_url = cmd.execute()
    db_shortened_url = ShortenedURL.get_by_id(shortened_url.id)

    assert db_shortened_url.id == shortened_url.id
    assert db_shortened_url.url == shortened_url.url

def test_create_shortened_url_already_exists():
    """
    GIVEN a CreateShortenedURL command with an existing URL
    WHEN the command is executed
    THEN a AlreadyExists exception is raised
    """
    ShortenedURL(url='http://example.com', short_url='http://example.com').save()

    cmd = CreateShortenedURLCommand(url='http://example.com')

    with pytest.raises(AlreadyExists):
        cmd.execute()
