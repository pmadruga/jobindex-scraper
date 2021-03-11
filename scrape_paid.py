from sqlalchemy.sql import text
from helpers import remove_blank_lines


def scrape_paid(soup, engine):
    job_postings_paid = soup.find_all("div", class_="PaidJob")
    # print("found {0} paid jobs".format(len(job_postings_paid)))

    for index, job in enumerate(job_postings_paid):
        # print(index+1)
        job_company_rating_amount = None
        job_company_rating = None
        job_ratings_link = None
        job_description = ""
        job_description_img = None
        job_company = None
        job_title = None
        job_location = None

        job_date = job.find("time").attrs["datetime"] if job.find("time") else job_date
        job_link = job.find("a", href=True)["href"]

        if job.find("img") != None:
            job_description_img = job.find("img")["src"]

        # job description inside <p>'s
        for (index, value) in enumerate(job.find_all("p")):
            job_description += value.get_text()

        # job description <ul>
        for list in job.find_all("ul"):
            # exclude the bottom div (which has <ul>'s)
            if list.attrs.get("class") == None:
                job_description += list.get_text()

        for (index, value) in enumerate(job.find_all("a")):

            if index == 0:
                if value.find("b") != None:
                    job_title = value.find("b").get_text()
                if value.find("b") == None and len(value.contents) > 0:
                    job_title = value.string

            if index == 1:
                if value.find("b") != None and job_title == None:
                    job_title = value.find("b").get_text()
                if value.find("b") != None and job_title != None:
                    job_company = value.find("b").get_text()

            if index == 2 and job_location == None:
                if value.find("b") != None:
                    job_company = value.find("b").get_text()

                if value.next_sibling != None:
                    try:
                        job_location = value.next_sibling.strip(", ")
                    except:
                        job_location = None

                else:
                    job_location = None

                if job_title == None and value.find("b") != None:
                    job_title = value.find("b").get_text()

            if (
                index == 3
                and value.find("b")
                and job_location != None
                and len(job_location) < 2
            ):
                job_location = value.find("b").get_text()

        if job.find(class_="num-ratings") != None:
            job_company_rating = job.find("span", class_="sr-only").get_text()
            job_ratings_link = job.find("a", class_="num-ratings", href=True)["href"]
            job_company_rating_amount = int(
                job.find("a", class_="num-ratings").get_text()
            )

        if (
            job_company == None
            and len(job.find_all("p")) > 0
            and job.find_all("p") != None
            and job.find_all("p")[0] != None
            and job.find_all("p")[0].find("b") != None
        ):
            job_company = job.find_all("p")[0].find("b").get_text()

        if (
            job_location == None
            and len(job.find_all("p")) > 0
            and job.find_all("p") != None
            and job.find_all("p")[0] != None
            and job.find_all("p")[0].find("b") != None
            and job.find_all("p")[0].find("b").next_sibling != None
        ):
            job_location = job.find_all("p")[0].find("b").next_sibling.strip(", ")

        if job_title == None:
            job_title = "no_title"

        print(job_title, job_location, job_date)

        query = text(
            "INSERT INTO jobindex_2021(title, company, location, description, description_img, source, date, company_rating, company_rating_amount, ratings_link, link, type) VALUES(:title, :company, :location, :description, :description_img, :source, :date, :company_rating, :company_rating_amount, :ratings_link, :link, :type)"
        )

        engine.connect().execute(
            query,
            {
                "title": job_title,
                "company": job_company,
                "location": job_location,
                "description": remove_blank_lines(string=job_description),
                "description_img": job_description_img,
                "source": None,
                "date": job_date,
                "company_rating": job_company_rating,
                "company_rating_amount": job_company_rating_amount,
                "ratings_link": job_ratings_link,
                "link": job_link,
                "type": "paid",
            },
        )

    # return last_job_date
