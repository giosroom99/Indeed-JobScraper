# Indeed-JobScraper
A very basic web scraper. 

This web scraper scrapes Indeed.com to find jobs based on three criteria, and returns a list of jobs posted in the last 24H. 
The job search results are then saved as CSV files as Dataframe using Panda Library.
Then an email is sent to the end-user with the atatched CSV file.

    Tool and Technology used in this program
        Python Libraries: BeautifulSoup, requests, pandas, and STMP mail
        Hosted on PythonAnywhere cloud server.


    Error Handling 
           I have designed 2 error reporting tools for this project. An email error report that the user gets whenever an error occurs 
           at the run time of the program and a CSV error log, errors logs are saved in the CSV file and stored on the server in case the mail server fails.


    Future Functionality

            Data storage: MySQL cloud-based.
            Data visualization: Grafana will be used to visualize data from the database through a dashboard.
            Design UI.
