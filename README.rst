===========
scrape-jobs
===========


    Simple CLI jobs scraper



DISCLAIMER
==========


    * Made as POC

    * USE AT YOUR OWN RISK



Workflow
--------


    1. Scrape jobs matching certain criteria

        * linkedin.com - [ keywords , location ]

        * seek.com.au - [ what , where ]


    2. Store the scraped data

        * upload to Google Sheets.

        * or just store it locally to CSV file.



Installation
============


Prerequisites:

    * Google Chrome installed

    * chromedriver binary executable in PATH

    * Python 3.6+

    * Prepared Google Spreadsheet (detailed instructions bellow)


Install command:

    `pip install --force -U scrape-jobs`


Installs the following CLI bindings:


    * `scrape-jobs-init-config`

    * `scrape-jobs`



Basic Instructions
==================


1. Open terminal/CMD and 'cd' into working dir.

2. Run `scrape-jobs-init-config` to populate sample config file in the current work dir

    usage: scrape-jobs-init-config [-h] [--version] [-v] [-vv] [-f FILE]

    initialize sample 'scrape-jobs' config file

    optional arguments:
      -h, --help           show this help message and exit
      --version            show program's version number and exit
      -v, --verbose        set loglevel to INFO
      -vv, --very-verbose  set loglevel to DEBUG
      -f FILE              defaults to '/current/work/dir/scrape-jobs.ini'


3. Edit the config file as per your needs

4. Run `scrape-jobs` to trigger execution

    usage: scrape-jobs [-h] [--version] [-v] [-vv] [-c CONFIG_FILE]
                       {linkedin.com,seek.com.au}

    Scrape jobs and store results.

    positional arguments:
      {linkedin.com,seek.com.au}
                            site to scrape

    optional arguments:
      -h, --help            show this help message and exit
      --version             show program's version number and exit
      -v, --verbose         set loglevel to INFO
      -vv, --very-verbose   set loglevel to DEBUG
      -c CONFIG_FILE        defaults to '/current/work/dir/scrape-jobs.ini'


More Detailed Instructions:
---------------------------

- Prepare the spreadsheet and the spreadsheet's auth.json (Spreadsheet instructions at the bottom)

    - For `seek.com.au` the Worksheet's columns are:

        ["scraped_time", "posted_time", "location", "area", "classification", "sub_classification", "title", "salary", "company", "url"]

    - For `linkedin.com` the Worksheet's columns are:

         ["scraped_time", "posted_time", "location", "title", "company", "url"]

- Init empty config file by calling `scrape-jobs-init-config`

- Edit the newly created `CWD\\scrape-jobs.ini` with params of your choice

    - set the path to the AUTH.JSON

    - set the spreadsheet name

    - set the worksheet name  (it will be automatically created if it doesn't exist)

    - set the search params

- Trigger execution:

    - run `scrape-jobs linkedin.com` or `scrape-jobs seek.com.au`

    - you will see output in the console, but a scrape-jobs.log will be created too

    - to have more detailed output add `-vv` execution param

- After the scrape is complete you should see the newly discovered jobs in your spreadsheet

- Alternatively you can init a config at a known place and just pass it's path:

    `scrape-jobs-init-config -f /custom/path/to/config.ini`

    `scrape-jobs -c /custom/path/to/config.ini seek.com.au`



Note
====


You need to prepare AUTH.JSON file in advance that is to be used for authentication with GoogleSheets

The term 'Spreadsheet' refers to a single document that is shown in the GoogleSpreadsheets landing page

A single 'Spreadsheet' can contain one or more 'Worksheets'

Usually a newly created 'Spreadsheet' contains a single 'Worksheet' named 'Sheet1'

If you don't provide a valid path to AUTH.JSON the collected data will be saved as .csv in the current work dir



Instructions for preparing Google Spreadsheet AUTH.JSON:
--------------------------------------------------------


    1. Go to https://console.developers.google.com/

    2. Login with the google account that is to be owner of the 'Spreadsheet'.

    3. At the top-left corner, there is a drop-down right next to the "Google APIs" text

    4. Click the drop-down and a modal-dialog will appear, then click "NEW PROJECT" at it's top-right

    5. Name the project relevant to how the sheet is to be used, don't select 'Location*', just press 'CREATE'

    6. Open the newly created project from the same drop-down as in step 3.

    7. There should be 'APIs' area with a "-> Go to APIs overview" at it's bottom - click it

    8. A new page will load having '+ ENABLE APIS AND SERVICES' button at the top side's middle - click it

    9. A new page will load having a 'Search for APIs & Services' input - use it to find and open 'Google Drive API'

    10. In the 'Google Drive API' page click "ENABLE" - you'll be redirected back to the project's page

    11. There will be a new 'CREATE CREDENTIALS' button at the top - click it

    12. Setup the new credentials as follows:

        - Which API are you using? -> 'Google Drive API'

        - Where will you be calling the API from? -> 'Web server (e.g. node.js, Tomcat)

        - What data will you be accessing? -> 'Application data'

        - Are you planning to use this API with App Engine or Compute Engine? -> No, I'm not using them.

    13. Click the blue button 'What credentials do I need', will take you to 'Add credentials to you project' page

    14. Setup the credentials as follows:

        - Service account name:  {whatever name you type is OK, as long the input accepts it}

        - Role: Project->Editor

        - Key type: JSON

    15. Press the blue 'Continue' button, and a download of the AUTH.JSON file will begin (store it safe)

    16. Close the modal and go back to the project 'Dashboard' using the left-side navigation panel

    17. Repeat step 8.

    18. Search for 'Google Sheets API', then open the result and click the blue 'ENABLE' button

    19. Open the downloaded auth.json file and copy the value of the 'client_email'

    20. Using the same google account as in step 2. , go to the normal google sheets and create & open the 'Spreadsheet'

        - do a final renaming to the spreadsheet now to avoid issues in future

    21. 'Share' the document with the email copied in step 19., giving it 'Edit' permissions

        - you might want to un-tick 'Notify people' before clicking 'Send' as it's a service email you're sharing with

        - 'Send' will change to 'OK' upon un-tick, but we're cool with that - just click it.

    You are now ready to use this class for retrieving 'Spreadsheet' handle in the code!
