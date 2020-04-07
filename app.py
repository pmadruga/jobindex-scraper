from flask import Flask

# from sqlalchemy import create_engine
from scrape import run
import os

app = Flask(__name__)

app.config.from_object(os.environ["APP_SETTINGS"])
# engine = create_engine(os.environ['DATABASE_URL'])


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/start")
def start():
    run(page_number=1, min_date="20000101", max_date="20070316")
    return "finished!"


if __name__ == "__main__":
    app.run()
