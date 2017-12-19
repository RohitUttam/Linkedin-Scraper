import argparse, os, time
from urllib.parse import urlparse
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import csv

#Login to Linkedin
EMAIL=input('Linkedin Email:')
PASSWORD=input('Linkedin Password:')

browser=webdriver.Chrome()
browser.get("https://linkedin.com/uas/login")

emailElement=browser.find_element_by_id("session_key-login")
emailElement.send_keys(EMAIL)
passElement = browser.find_element_by_id("session_password-login")
passElement.send_keys(PASSWORD)
passElement.submit()

os.system('cls')
print("[+] Successfully logged in!")
time.sleep(random.uniform(4,10.9))

#LinkedInSearch
browser.get("https://www.linkedin.com/jobs/search/?keywords=Multinational&location=Germany&locationId=de%3A0")
page =BeautifulSoup(browser.page_source)

#Get Job links
def getJobLinks(page):
	links=[]
	for link in page.find_all("a", class_="job-card-search__link-wrapper js-focusable-card ember-view"):
		url=link.get('href')
		if url:
			if '/jobs' in url:
				links.append(url)
	return links

jobs=getJobLinks(page)
jobs=jobs[::2]
ejobs=[]
names=[]
jobtitles=[]
companies=[]

#for each Job, get the job poster name, company and jobtitle
for i in jobs:
    ljobs='http://www.linkedin.com'+ i
    ejobs.append(ljobs)
    browser.get(ljobs)
    time.sleep(random.uniform(4, 10.9))
    page =BeautifulSoup(browser.page_source)
    name = page.find_all("p", class_="jobs-poster__name name Sans-17px-black-85%-semibold mb0")
    if len(name)== 0:
        names.append('Not available')       
    else:
        name = name[0].text
        name=name.strip('\n')
        names.append(name.strip())

    jobtitle = page.find_all("p", class_="jobs-poster__headline Sans-17px-black-70%-dense mb0")
    if len(jobtitle) == 0:
       jobtitles.append('Not available')
        
    else:
        jobtitle = jobtitle[0].text
        jobtitle= jobtitle.strip('\n')
        jobtitles.append(jobtitle.strip())

    company=page.find_all("a", class_="jobs-details-top-card__company-url ember-view")
    if len(company) == 0:
        companies.append('No contact available')
    else:
        company = company[0].text
        company=company.strip('\n')
        companies.append(company.strip())

#insert header
names.insert(0,"NAMES")
jobtitles.insert(0,"JOBTITLES:")
companies.insert(0,"COMPANY NAMES:")

#write .csv file
with open('linkedin.csv', 'w', newline='') as f:
        linwriter= csv.writer(f)
        linwriter.writerow(names)
        linwriter.writerow(jobtitles)
        linwriter.writerow(companies)






