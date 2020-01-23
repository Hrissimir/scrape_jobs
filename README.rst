===========
scrape_jobs
===========


CLI jobs scraper targeting multiple sites



Description
===========


Extract jobs details from a target site and upload data to google sheets.


Currently supported sites
-------------------------

- linkedin.com
- seek.com.au


Installation
------------

`pip install --force -U scrape_jobs`


Short instructions:
-------------------

- Ensure your machine has available chromedriver in path
- Prepare upload spreadsheet (detailed instructions bellow)
- Open cmd / terminal
- Install / Update from pip with `pip install --force -U scrape_jobs`
- Call `scrape-jobs-init-config` to get sample 'scrape-jobs.ini' file in the current dir
- Edit the config file and save
- Call `scrape-jobs -s TARGET_SITE -c scrape-jobs.ini` and let it roll
- Check your spreadsheet after execution completes


Long Instructions:
------------------

- Prepare the spreadsheet and the spreadsheet's secrets .json (instructions at the bottom)

    - In seek.com.au results sheet, set the first row values (the header) to:

        'date', 'location', 'title', 'company', 'classification', 'url', 'is_featured', 'salary'

- Open a cmd/terminal

- Navigate to some work folder of your choice (e.g "c:\job_scrape", referred to later as CWD)

- Init empty config file by calling `scrape-jobs-init-config`

- Edit the newly created `CWD\\scrape-jobs.ini` with params of your choice

    - set the path to the CREDENTIALS SECRETS .JSON

    - set the proper spreadsheet name

    - set the index of the worksheet where you want the results to be uploaded (0-based index)

- To trigger execution:

    - run `scrape-jobs -s TARGET_SITE -c scrape-jobs.ini`

    - you will see output in the console, but a scrape-jobs.log will be created too

    - to have more detailed output call `scrape-jobs -vv -s TARGET_SITE -c scrape-jobs.ini` instead

- After the scrape is complete you should see the newly discovered jobs in your spreadsheet

- Alternatively you can init a config at a known place and just pass it's path:

    `scrape-jobs -s seek.com.au -c /path/to/config.ini`


Note
====

You need to prepare secrets .json file in advance that is to be used for authentication with GoogleSheets

The term 'Spreadsheet' refers to a single document that is shown in the GoogleSpreadsheets landing page

A single 'Spreadsheet' can contain one or more 'worksheets'

Usually a newly created 'Spreadsheet' contains a single 'worksheet' named 'Sheet1'


Instructions for preparing a shared Google Spreadsheet CREDENTIALS SECRETS .JSON:
---------------------------------------------------------------------------------

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

    15. Press the blue 'Continue' button, and a download of the CREDENTIALS SECRETS .JSON file will begin (store it safe)

    16. Close the modal and go back to the project 'Dashboard' using the left-side navigation panel

    17. Repeat step 8.

    18. Search for 'Google Sheets API', then open the result and click the blue 'ENABLE' button

    19. Open the downloaded secrets.json file and copy the value of the 'client_email'

    20. Using the same google account as in step 2. , go to the normal google sheets and create & open the 'Spreadsheet'

        - do a final renaming to the spreadsheet now to avoid coding issues in future

    21. 'Share' the document with the email copied in step 19., giving it 'Edit' permissions

        - you might want to un-tick 'Notify people' before clicking 'Send' as it's a service email you're sharing with

        - 'Send' will change to 'OK' upon un-tick, but we're cool with that - just click it.

    You are now ready to use this class for retrieving 'Spreadsheet' handle in the code!
