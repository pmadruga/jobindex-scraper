from flask import Flask
from sqlalchemy import create_engine
from scrape import run
import os

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
engine = create_engine(os.environ['DATABASE_URL'])

@app.route('/')
def hello():
    return "Hello World!"


@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

@app.route('/start/<date>')
def start(date):
    run(1, '20020101')
    return 'hey'

if __name__ == '__main__':
    app.run()
