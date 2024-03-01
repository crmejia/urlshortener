import pytest
from urlshortener.models import NotFound, ShortenedURL
from urlshortener.queries import GetShortenedURLByShortURLQuery, GetShortenedURLByURLQuery, ListShortenedURLsQuery, GetShortenedURLByIdQuery
from urlshortener.commands import Hash_url

def test_list_shortenedURLs():
    """
    GIVEN 2 shortenedURLS stored in the DB
    WHEN the query is executed
    THEN a list of  2 ShortenedURLs is returned
    """

    ShortenedURL(url='http://example.com', short_url='http://example.com').save()
    ShortenedURL(url='http://example2.com', short_url='http://example2.com').save()

    query = ListShortenedURLsQuery()
    shortened_urls = query.execute()

    assert len(shortened_urls) == 2
    assert shortened_urls[0].url == 'http://example.com'
    assert shortened_urls[1].url == 'http://example2.com'

def test_list_shortenedURLs_empty():
    """
    GIVEN no shortenedURLS stored in the DB
    WHEN the query is executed
    THEN an empty list is returned
    """

    query = ListShortenedURLsQuery()
    shortened_urls = query.execute()

    assert len(shortened_urls) == 0 

def test_get_shortenedURL_by_id():
    """
    GIVEN ID of a shortenedURL stored in the DB
    WHEN the execute mthod is called of GetShortenedURLByIdQuery with an ID
    THEN it should return the shortenedURL with the same ID
    """
    shortened_url = ShortenedURL(url='http://example.com', short_url='http://example.com')
    shortened_url.save()

    query = GetShortenedURLByIdQuery(id=shortened_url.id)

    assert query.execute().id == shortened_url.id

def test_get_shortenedURL_by_short_url():
    """
    GIVEN short_url of a shortenedURL stored in the DB
    WHEN the execute method is called of GetShortenedURLByShortURLQuery with an short_url
    THEN it should return the shortenedURL with the same short_url
    """
    short_url = Hash_url('http://example.com')
    shortened_url = ShortenedURL(url='http://example.com', short_url=short_url)
    shortened_url.save()

    query = GetShortenedURLByShortURLQuery(short_url=short_url)

    assert query.execute().short_url == short_url

def test_get_shortenedURL_by_short_url_raises_NotFound():
    """
    GIVEN a short_url not stored in the DB
    WHEN the execute method is called of GetShortenedURLByShortURLQuery with an short_url
    THEN it should return raise a NotFound exception
    """
    short_url = Hash_url('http://example.com')

    query = GetShortenedURLByShortURLQuery(short_url=short_url)

    with pytest.raises(NotFound):
        query.execute() 

def test_get_shortenedURL_by_url():
    """
    GIVEN url of a shortenedURL stored in the DB
    WHEN the execute method is called of GetShortenedURLByURLQuery with an url
    THEN it should return the shortenedURL with the same url
    """
    url = 'http://example.com'
    short_url = Hash_url(url)
    shortened_url = ShortenedURL(url=url, short_url=short_url)
    shortened_url.save()

    query = GetShortenedURLByURLQuery(url=url)

    assert query.execute().url == url

def test_get_shortenedURL_by_url_raises_NotFound():
    """
    GIVEN a url not stored in the DB
    WHEN the execute method is called of GetShortenedURLByURLQuery with an url
    THEN it should return raise a NotFound exception
    """
    url = Hash_url('http://example.com')

    query = GetShortenedURLByURLQuery(url=url)

    with pytest.raises(NotFound):
        query.execute() 
