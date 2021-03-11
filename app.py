from flask import Flask

# from sqlalchemy import create_engine
from scrape import run
import os

app = Flask(__name__)

# dummy date just for the jobindex url 
end_date = "20000101"
# it scrapes backwards in date
from_date = "20140509"

app.config.from_object(os.environ["APP_SETTINGS"])
# engine = create_engine(os.environ['DATABASE_URL'])


@app.route("/ping")
def ping():
    return 'pong'

@app.route("/start")
def start():
    # this didn't need to be an api but here we are.
    run(page_number=1, min_date=end_date, max_date=from_date)
    return "finished!"


if __name__ == "__main__":
    print("running from: {0}".format(from_date))
    app.run()
