def scrape_unpaid(soup):
    job_postings_free = soup.find_all('div', class_='jix_robotjob')

    for (index, job) in enumerate(job_postings_free):
        print(index+1)
        
        job_company_rating_amount = None
        job_company_rating = None
        job_ratings_link = None
        
        job_title = job.find('strong').get_text()
        job_link = job.find('a', href=True)['href']
        # get company and location
        if len(job.find_all('b')) == 2:
            job_company = job.find_all('b')[0].get_text()
            job_location = job.find_all('b')[1].get_text()
        else:
            job_company = None
            job_location = job.find_all('b')[0].get_text()
            

        if(job.find('img') != None):
            job_description = job.find('img').next_sibling
            job_description_img = job.find('img')['src']
        else:
            job_description = job.find_all('br')[0].next_sibling
            job_description_img = None
        job_poster = job.find('cite').get_text()
        job_date = job.find('time').attrs['datetime']
        
        if(job.find(class_='num-ratings') != None):
            job_company_rating = job.find('span', class_='sr-only').get_text()
            job_ratings_link = job.find('a', class_='num-ratings', href=True)['href']
            job_company_rating_amount = job.find('a', class_='num-ratings').get_text()

        
        ## return or write to database
        return {
            "job_title": job_title, 
            "job_company": job_company,
            "job_location": job_location, 
            "job_description": job_description,
            "job_description_img": job_description_img,
            "job_poster": job_poster,
            "job_date": job_date,
            "job_company_rating": job_company_rating, 
            "job_company_rating_amount": job_company_rating_amount, 
            "job_description": job_description, 
            "job_ratings_link": job_ratings_link, 
            "job_link": job_link}
