import json
import pathlib

import pytest
from jsonschema import validate, RefResolver

from urlshortener.app import app
from urlshortener.models import ShortenedURL
from urlshortener.commands import Hash_url

@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

def validate_payload(payload, schema_name):
    """
    Validate the payload against the schema
    """
    schema_dir = str(f"{pathlib.Path(__file__).parent.absolute()}/schemas")
    schema = json.loads(pathlib.Path(f"{schema_dir}/{schema_name}.json").read_text())
    validate(
        payload,
        schema,
        resolver=RefResolver(
            "file://" + str(pathlib.Path(f"{schema_dir}/{schema_name}").absolute()),
            schema
            )
        )

def test_create_shortened_url(client):
    """
    GIVEN a request to shorten a valid URL
    WHEN endpoint /shorten is called
    THEN a new ShortenedURL is returned in json format that matches the schema
    """

    response = client.post(
        '/shorten',
       data=json.dumps(
           {'url': 'http://example.com'},
        ),
        content_type='application/json',
    )

    assert response.status_code == 201

    validate_payload(response.json, 'ShortenedURL')

def test_get_shortened_url(client):
    """
    Given a short URL stored in the database
    WHEN endpoint /shortenedURL is called
    THEN a shortened URL is returned in json format that matches the schema
    """
    short_url = Hash_url('http://example.com')
    shortened_url = ShortenedURL(url='http://example.com', short_url='f0e6a6').save()

    response = client.get(f'/{short_url}', content_type='application/json')
    validate_payload(response.json, 'ShortenedURL')

def test_list_shortened_urls(client):
    """
    GIVEN a request to list all shortened URLs
    WHEN endpoint /shortenedURls is called
    THEN a list of ShortenedURLs is returned in json format that matches the schema
    """
    ShortenedURL(url='http://example.com', short_url='http://example.com').save()
    ShortenedURL(url='http://example2.com', short_url='http://example2.com').save()

    response = client.get('/shortenedURLs', content_type='application/json')

    assert response.status_code == 200
    validate_payload(response.json, 'ShortenedURLs')

def test_create_shortened_url_already_exists(client):
    """
    GIVEN a request to shorten an existing URL
    WHEN endpoint /shorten is called
    THEN a 200 status code is returned(idempotent behavior)
    """

    short_url = Hash_url('http://example.com')
    shortened_url = ShortenedURL(url='http://example.com', short_url='f0e6a6').save()

    response = client.post(
        '/shorten',
        data=json.dumps(
            {'url': 'http://example.com'},
        ),
        content_type='application/json',
    )

    assert response.status_code == 200
    validate_payload(response.json, 'ShortenedURL')

@pytest.mark.parametrize(
    'data',
    [
        {'url': ''},
        {'url': None},
    ]
)
def test_create_shortenedURL_bad_request(client, data):
    """
    GIVEN a request to shorten a URL with a missing field
    WHEN endpoint /shorten is called
    THEN a 400 status code is returned
    """
    response = client.post(
        '/shorten',
        data=json.dumps(data),
        content_type='application/json',
    )

    assert response.status_code == 400
    assert response.json is not None