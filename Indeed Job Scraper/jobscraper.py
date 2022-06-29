# Giovanni Thsibangu
# Python Indeed Web Scraper
# 3/16/2022

import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
from datetime import *
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import mimetypes
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
import time


# In[46]:

# Date and time object
today =date.today()
now =datetime.now().strftime("%H:%M:%S")

# Data frame and series Utilities
template  = {"Job Title":[],"Company Name":[],"Location":[],"Salaries":[],"Link":[]}
errorTemplate={"Eror":[],"Location":[],"Date":[],"Time":[]}
errorDataFrame= pd.DataFrame(errorTemplate)
Main_DataFrame =pd.DataFrame(template)

# Initiliaze variables
error_reporter=""
error_location=""
url=""
names=[]
titles=[]
links=[]
locations=[]
salaries=[]


# In[ ]:

# In[47]:

def getPage(url):

    try:
        page = requests.get(url)
        page.raise_for_status()
        soup = BeautifulSoup(page.content,'html.parser')
        result = soup.find(id="mosaic-provider-jobcards")
        job_elements = result.find_all("div", class_="job_seen_beacon")

        error_reporter="Success Soup"
        error_location="GetPage URL"
        errorLog_file(error_reporter,error_location,today,now)
        soup = BeautifulSoup(page.content,'html.parser')
        result = soup.find(id="mosaic-provider-jobcards")
        job_elements = result.find_all("div", class_="job_seen_beacon")

    except Exception as ex:

        error_reporter= str(ex)
        error_location="Soup"
        errorLog_file(error_reporter,error_location,today,now)
        message=error_reporter+" in the "+error_location+" Time "+str(today)+" "+str(now)

        email_Update("error","getPage "+error_reporter)
        print("An error as occured in the Soup: ")
    else:
        print("Soup elements have been successfuly scraped.")
        return soup

def jobCard(url):
    try:
        soup =getPage(url)
    except Exception as ex:
        error_reporter=str(ex)
        error_location="getPage Function Failed"
        errorLog_file(error_reporter,error_location,today,now)
        message=error_reporter+" in the "+error_location+" Time "+str(today)+" "+str(now)
        email_Update("error","jobCard "+error_reporter)
    else:
        title_element = soup.find_all("h2", class_="jobTitle")
        company_element = soup.find_all("span", class_="companyName")
        location_element = soup.find_all("div", class_="companyLocation")
        salary = soup.find_all("div", class_="attribute_snippet")
        job_link = soup.find_all("a", class_="tapItem")

        for title in title_element:
            titles.append(title.text)
        for name in company_element:
            names.append(name.text)
        for location in location_element:
            locations.append(location.text)
        for salar in salary:
            salaries.append(salar.text)
        for link in job_link:
            links.append("https://www.indeed.com"+link.get("href"))

        print("Success Job card  data")

        error_reporter="Success Jobcard"
        error_location="JobCard"
        errorLog_file(error_reporter,error_location,today,now)
        return (titles,names,locations,salaries,links)

def createDataFrame(url):
    try:
        jobCard(url)
        df_titles=pd.Series(titles,name="Job Title")
        df_names=pd.Series(names,name="Company Name")
        df_locations=pd.Series(locations,name="Location")
        df_salaries=pd.Series(salaries,name="Salaries")
        df_job_link=pd.Series(links,name="Links")
        # Frame contains all the row required for our dataFrame
        frames =[df_titles,df_names,df_locations,df_salaries,df_job_link]
        # Concat all.
        job_card =pd.concat(frames,axis=1)
        print("Data Frame successfull created")
    except Exception as ex:
        error_reporter=str(ex)
        error_location="createDataFrame"
        message=error_reporter+" in the "+error_location+" Time "+str(today)+" "+str(now)
        errorLog_file(error_reporter,error_location,today,now)
        email_Update("error","createDataFrame "+error_reporter)
        print(ex)
    else:
            # Return dataFrame
        return job_card
# In[54]:

# Email Function
def email_Update(file,subject):
    emailfrom = "<Your email>"
    emailto ="<Recipient email>"
    fileToSend = file+".csv"
    username = "user"
    password = "<Your password>"

    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = emailto
    msg["Subject"] = subject
    msg.preamble = subject

    ctype, encoding = mimetypes.guess_type(fileToSend)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"

    maintype, subtype = ctype.split("/", 1)

    if maintype == "text":
        fp = open(fileToSend)
        # Note: we should handle calculating the charset
        attachment = MIMEText(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "image":
        fp = open(fileToSend, "rb")
        attachment = MIMEImage(fp.read(), _subtype=subtype)
        fp.close()
    elif maintype == "audio":
        fp = open(fileToSend, "rb")
        attachment = MIMEAudio(fp.read(), _subtype=subtype)
        fp.close()
    else:
        fp = open(fileToSend, "rb")
        attachment = MIMEBase(maintype, subtype)
        attachment.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(attachment)
    attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
    msg.attach(attachment)

    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login(emailfrom,password)
    server.sendmail(emailfrom, emailto, msg.as_string())
    print("Quitting the Server!!!")
    server.quit()
# In[55]:

def errorLog_file(error,loc,date,time):
    try:
        errorTemplate={"Eror":[error],"Location":[loc],"Date":[date],"Time":[time]}
        errorDataFrame= pd.DataFrame(errorTemplate)

    except Exception as ex:
        error_reporter=str(ex)
        error_location="Driver main"
        message=error_reporter+" in the "+error_location+" Time "+str(today)+" "+str(now)

        email_Update("error","ErrorLog_File "+error_reporter)
    else:
        errorDataFrame.to_csv("error.csv")
# In[56]:
def DriverMain(listOfposition):
    try:
        for job_title in listOfposition:
            city="waterbury"
            state="CT"
            url ="https://www.indeed.com/jobs?q={job_title}&l={city}%2C%20{state}&fromage=1&".format(job_title=job_title,city=city,state=state)

            file = createDataFrame(url)

            file.to_csv(job_title+".csv")
            email_Update(job_title,"Job Update!")
            print(url)
            print(job_title+" Job  CSV created Email sent!")
            time.sleep(10)
    except Exception as ex:
        print("Failed link: "+url)
        print(ex)
        error_reporter=str(ex)
        error_location="Driver main"
        message=error_reporter+" in the "+error_location+" Time "+str(today)+" "+str(now)
        email_Update("error","DriverMain "+error_reporter)
        errorLog_file(error_reporter,error_location,today,now)
    else:
        print(job_title," Job file has been searched and saved as csv ")
        print()
# In[59]:


listOfposition=["Developer","Programmer","software"] # List of job titles to search
DriverMain(listOfposition)      # Driver function
