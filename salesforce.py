# Prerequisites:

# Python Crash Course: https://www.youtube.com/watch?v=-FS0CzffP8E
# Install Python, Pip: https://www.youtube.com/watch?v=lnse_uD-MaA
# INSTALL Simple Saleforce Library
# Install: https://pypi.org/project/simple-salesforce/ OR (pip install simple-salesforce)
# Python Simple Salesforce Library Documentation: https://pypi.org/project/simple-salesforce/
# Official Salesforce Documentation:
#   https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/intro_what_is_rest_api.htm

# Obtain a security token
# At the top navigation bar go to your name > Settings > Reset My Security Token -> Get Token from email


# IMPORT ANY LIBRARIES NEEDED
import json
from pprint import pprint
from simple_salesforce import Salesforce, format_soql, SalesforceMalformedRequest

# SALEFORCE AUTHENTICATION

credentials = json.load(open('credentials.json'))
sf = Salesforce(
    username=credentials['username'],
    password=credentials['password'],
    security_token=credentials['security_token'],
    domain='login'
)

# GET AVAILABLE SALESFORCE TABLES

class Salesforce:
    def get_all_salesforce_tables(self):
        s_objects = []

        data = sf.query_all_iter(query='SELECT SObjectType FROM ObjectPermissions')
        print('Available Tables')
        count = 0
        for row in data:
            count += 1
            s_objects.append(row['SobjectType'])

        print('Returned ' + str(count) + ' columns. Showing 10 results')
        pprint(s_objects[0: 10])
        return s_objects


    def get_all_columns(self, table):
        """
        GET AVAILABLE COLUMNS FOR SPECIFIED TABLE
        """
        columns = []
        data = sf.query_all_iter(query="SELECT QualifiedApiName FROM FieldDefinition WHERE EntityDefinition.QualifiedApiName IN ('" + table + "')")

        print('Available Fields')
        count = 0
        for row in data:
            count += 1
            columns.append(row['QualifiedApiName'])

        print('Returned ' + str(count) + ' columns. Showing 10 results')
        pprint(columns[0: 10])
        return columns

    # SOQL QUERY
    def get_salesforce_data_from_query(self, soql_query):
        data = sf.query_all_iter(query=soql_query)
        return data

    def build_query(self, table_name, column_list, where_clause=""):
        query = "SELECT "
        query += ", ".join(column_list)
        query += ' FROM ' + table_name
        if where_clause != "":
            query += " " + where_clause
        return query

    def get_salesforce_data(self, table_name, column_list, where_clause=""):
        query = self.build_query(table_name, column_list, where_clause)
        print('EXECUTING QUERY: ' + query)

        data = sf.query_all_iter(query=query)

        return data

    def build_pandas(self, data):
        pass

    def display_rows(self, rows_returned):
        rows = []

        for row in rows_returned:
            count = 0
            rows.append(row)

        print("Printing data showing 10 rows")

        pprint(rows[0: 10])

s_f = Salesforce()

# SELECT column_name FROM table_name

try:
    my_data = s_f.get_salesforce_data('my_table', ["abc", "123", "more"], "WHERE abc=123")
    row_count = 0
    for row in my_data:
        row_count += 1
        print(row)

    print(f"Query returned: {row_count} rows.")

except SalesforceMalformedRequest as s:
    print('Malformed Query')
    # Remove next line to print exception
    # print(s)

tables = s_f.get_all_salesforce_tables()

columns = s_f.get_all_columns('Account')

try:
    # rows_returned = s_f.get_salesforce_data(tables[0], columns[0: 10])
    rows_returned =   s_f.get_salesforce_data('Account', ["Id", "IsDeleted"], "WHERE Id != ''")



    s_f.display_rows(rows_returned)
except SalesforceMalformedRequest as s:
    print('Malformed Query')

# Other tips:
# Convert your data to pandas data frame to easily parse and manipulate data.
# Documentation:
# https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html
