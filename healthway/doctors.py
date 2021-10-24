'''
Download list from https://mdsched.healthway.com.ph/ 
to excel
 
'''
import re

import requests
from time import sleep
from bs4 import BeautifulSoup
from requests.models import Response
from requests.sessions import session
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

MAX = 2
base_url = "https://mdsched.healthway.com.ph/"
ses = requests.Session()
response = ses.get(base_url,verify=False)
soup = BeautifulSoup(response.content, "html.parser")
rows = soup.select("table#mydatatable tbody > tr")

for index, row in enumerate(rows):
    print(list(row.stripped_strings))
    # btnviewdoctor(number)

    onclick = row.select_one('td > a').get('onclick')
    regex = r"^btnviewdoctor\((\d+)\)"
    match = re.search(regex, onclick)
    if match:
        # extract id
        id = match.group(1)

        # POST https://mdsched.healthway.com.ph/doctor_sched.php 
        # form-data
        # id: 

        # sub specialization, branch , day, time


        ses.headers.update({'referrer': base_url, "X-Requested-With": "XMLHttpRequest"})
        doc_response = ses.post("https://mdsched.healthway.com.ph/doctor_sched.php",data={'id': id}, verify=False)
        
        
        soup2 = BeautifulSoup(doc_response.content, 'html.parser')
        subtxt = soup2.find('strong',text="Sub-specialization:")
        print("Sub Specialty:", subtxt.next_sibling.next_sibling.text)
        print(soup2.find('tbody').text)
    

    

    if index+1 >= MAX: break


 
