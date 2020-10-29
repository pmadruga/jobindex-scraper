from sqlalchemy.sql import text
from helpers import remove_blank_lines


def scrape_unpaid(soup, engine):
    job_postings_free = soup.find_all("div", class_="jix_robotjob")
    last_post_date = None

    for (index, job) in enumerate(job_postings_free):
        job_company_rating_amount = None
        job_company_rating = None
        job_ratings_link = None
        job_description_img = None
        job_company = None
        job_location = None

        job_title = job.find("strong").get_text()
        job_link = job.find("a", href=True)["href"]

        # get company and location
        if len(job.find_all("b")) == 2 and job.find_all("b"):
            job_company = job.find_all("b")[0].get_text()
            job_location = job.find_all("b")[1].get_text()
        if len(job.find_all("b")) != 2 and job.find_all("b"):
            job_company = None
            job_location = job.find_all("b")[0].get_text()

        if job.find("img") != None:
            job_description = job.find("img").next_sibling
            job_description_img = job.find("img")["src"]
        else:
            job_description = job.find_all("br")[0].next_sibling

        if(job.find('cite') != None):
            job_source = job.find("cite").get_text()
        
        job_date = job.find("time").attrs["datetime"]

        if job.find(class_="num-ratings") != None:
            job_company_rating = job.find("span", class_="sr-only").get_text()
            job_ratings_link = job.find("a", class_="num-ratings", href=True)["href"]
            job_company_rating_amount = int(
                job.find("a", class_="num-ratings").get_text()
            )

        print(job_title, job_location, job_date)

        last_post_date = job_date

        ## write to database
        query = text(
            "INSERT INTO jobindex(title, company, location, description, description_img, source, date, company_rating, company_rating_amount, ratings_link, link, type) VALUES(:title, :company, :location, :description, :description_img, :source, :date, :company_rating, :company_rating_amount, :ratings_link, :link, :type)"
        )

        engine.connect().execute(
            query,
            {
                "title": job_title,
                "company": job_company,
                "location": job_location,
                "description": remove_blank_lines(string=job_description),
                "description_img": job_description_img,
                "source": job_source,
                "date": job_date,
                "company_rating": job_company_rating,
                "company_rating_amount": job_company_rating_amount,
                "ratings_link": job_ratings_link,
                "link": job_link,
                "type": "unpaid",
            },
        )

    return last_post_date
