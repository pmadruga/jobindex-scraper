from flask import Flask

# from sqlalchemy import create_engine
from scrape import run
import os

app = Flask(__name__)

start_date = "20000101"
end_date = "20050711"

app.config.from_object(os.environ["APP_SETTINGS"])
# engine = create_engine(os.environ['DATABASE_URL'])


@app.route("/ping")
def ping():
    return 'pong'

@app.route("/start")
def start():
    run(page_number=1, min_date=start_date, max_date=end_date)
    return "finished!"


if __name__ == "__main__":
    print("running from: {0}".format(end_date))
    app.run()
