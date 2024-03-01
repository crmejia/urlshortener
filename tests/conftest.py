import os
import tempfile

import pytest

from urlshortener.models import ShortenedURL

@pytest.fixture(autouse=True)
def setup_database():
    _, db_name = tempfile.mkstemp()
    os.environ['DATABASE_NAME'] = db_name
    ShortenedURL.create_table(database_name=db_name)
    yield
    os.unlink(db_name)