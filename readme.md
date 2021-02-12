# Connector for Salesforce to SQL Server Using Python

## Introduction:

This project uses simple-salesforce python library to get data from Salesforce CRM. Use this repository to query Salesforce using SOQL query language. Also available in sql_server_connector.py is a package to help connect to Sql Server.

## Prerequisites:

###Helpful references
Python Crash Course: https://www.youtube.com/watch?v=-FS0CzffP8E

CodeCademy: https://www.codecademy.com

Install Python, Pip: https://www.youtube.com/watch?v=lnse_uD-MaA

Python Simple Salesforce Library Documentation: https://pypi.org/project/simple-salesforce/

Official Salesforce Documentation: https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/intro_what_is_rest_api.htm

Pandas Docs: https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html

### New Project Installation

**Python (Latest Version)**

**PIP Installation Packages**

For python and pip installation use references above.

**Simple Salesforce Library**

Guide: https://pypi.org/project/simple-salesforce/

OR

`pip install simple-salesforce`

See above for documentation


### Steps for getting started

1. Obtain a security token
   
    a. Login to Salesforce Developer or Create an account
   
    b. At the top navigation bar go to your name > Settings > Reset My Security Token -> Get Token from email
   
2. Fill out credentials

    a. Open credentials.example.json
   
    b. Copy the file using the command `cp credentials.example.json credentials.json` or copy and paste. The name of the file needs to be `credentials.json`

    c. Fill out credentials for salesforce as well as the security token obtained from salesforce above.

    d. Fill out credentials for sql server

3. Install required packages and libraries

    a. Open a terminal window in the location you downloaded this project.

    b. Run the command: `python -m pip install -r requirements.txt`

4. You are ready to run the program!

   a. Click run on the package in a text editor program

   b. Or run `python salesforce.py`


### Developer

```
Xantie Analytics
Josh Smith
josh@xantie.com
```