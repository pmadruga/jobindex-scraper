import requests
from bs4 import BeautifulSoup
from scrape_unpaid import scrape_unpaid

page_number_limit = 5

def build_url(min_date, max_date, page_number):
        return 'https://www.jobindex.dk/jobsoegning?maxdate=' + max_date + '&mindate=' + min_date + '&page=' + str(page_number) + '&archive=1'

def scrape(max_date, min_date, page_number):
    url = build_url(min_date, max_date, page_number)
    print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')


    ## do page request
    if (len(page.content) > 0):
        # print(soup) 
        ## fetch unpaid (fetch date and set it to min date when page number limit has been hit)

        ## fetch paid

        ## write to database

        return True
    
    
    return False
        


# while page_number == 1:
#     print(build_url(page_number='1', max_date='20201002', min_date='20020101'))

def format_date(date):
    return ('').join((date).split('-'))
    

def run(page_number, min_date):
    
    while (page_number <= page_number_limit):
        # break
        
        if (scrape(page_number=page_number, max_date='20201002', min_date=min_date) == True):
            page_number += 1
        else:
            ## set min_date here from the job posting
            return False
       
    
    run(page_number=1, min_date='20180101')
    
    
## initial conditions
min_date = '20020101'
page_number = 1

## run it
run(page_number, min_date)
