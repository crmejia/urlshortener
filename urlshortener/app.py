from flask import Flask, request

from urlshortener.commands import AlreadyExists, CreateShortenedURLCommand
from urlshortener.queries import GetShortenedURLByURLQuery, ListShortenedURLsQuery, GetShortenedURLByShortURLQuery

app = Flask(__name__)

@app.route('/shorten',methods=['POST'])
def shorten():
    cmd = CreateShortenedURLCommand(**request.json)
    try:
        shortened_url = cmd.execute()
    except AlreadyExists:
        shortened_url = GetShortenedURLByURLQuery(url=request.json['url']).execute()
        return shortened_url.model_dump(), 200

    return shortened_url.model_dump(), 201


@app.route('/shortenedURLs', methods=['GET'])
def list_shortened_urls():
    query = ListShortenedURLsQuery()
    data =[shortened_url.model_dump() for shortened_url in query.execute()] 
    return data

if __name__ == '__main__':
    app.run()

@app.route('/<short_url>', methods=['GET'])
def get_shortened_url(short_url):
    shortened_url = GetShortenedURLByShortURLQuery(short_url=short_url).execute()
    return shortened_url.model_dump()