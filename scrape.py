import requests
from bs4 import BeautifulSoup
from scrape_unpaid import scrape_unpaid
from scrape_paid import scrape_paid
from sqlalchemy import create_engine
import os

engine = create_engine(os.environ["DATABASE_URL"])

page_number_limit = 5000
last_known_result = None


def build_url(min_date, max_date, page_number):
    return (
        "https://www.jobindex.dk/jobsoegning?maxdate="
        + max_date
        + "&mindate="
        + min_date
        + "&page="
        + str(page_number)
        + "&archive=1"
    )


def scrape(max_date, min_date, page_number):
    last_known_date = max_date

    url = build_url(min_date, max_date, page_number)
    print("fetching data from url: {0}".format(url))
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    if soup.find("div", class_="PaidJob"):
        # global last_known_date
        last_known_date = (
            soup.find("div", class_="PaidJob").find("time").attrs["datetime"]
        )

    if soup.find("div", class_="jix_robotjob"):
        # global last_known_date
        last_known_date = (
            soup.find("div", class_="jix_robotjob").find("time").attrs["datetime"]
        )

    ## do page request
    if len(page.content) > 0:
        ## fetch unpaid
        scrape_unpaid(soup, engine)

        ## fetch paid
        scrape_paid(soup, engine)
        # print(last_known_date)

        return last_known_date

    return False


def format_date(date):
    return ("").join((date).split("-"))


def url_format_date(date):
    return ("").join(date.split("-"))


def run(page_number, min_date, max_date):
    # restart_batch_date = last_known_date

    # run batch of scrapes
    while page_number <= page_number_limit:

        last_known_result = scrape(
            page_number=page_number, max_date=max_date, min_date=min_date
        )

        # if the requests returns content
        if last_known_result != False:
            print("\n\n\n")
            print("last known date: {0}".format(last_known_result))
            # app.logger.info('%s logged in successfully', last_known_date)
            page_number += 1
        else:
            ## set min_date here from the job posting
            print("shows over!")
            # break
            return False

    proper_date = url_format_date(last_known_result)
    # when the batch is over, restart with last known date
    print("about to start a new batch. last known date is: {0}".format(proper_date))
    run(page_number=1, min_date=min_date, max_date=proper_date)
