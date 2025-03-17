"""
Module for extracting data from Google Sheets.
This module provides functionality to connect to Google Sheets API
and extract specific columns of data.
"""

from typing import Optional
import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

def connect_to_sheets():
    """
    Establishes connection to Google Sheets API using service account credentials.
    
    Returns:
        service: Google Sheets API service object
    """
    scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    creds = Credentials.from_service_account_file(
        'credentials.json',
        scopes=scopes
    )
    
    service = build('sheets', 'v4', credentials=creds)
    return service

def extract_sheet_data() -> Optional[pd.DataFrame]:
    """
    Extracts specified columns from the Google Sheet.
    
    Returns:
        pd.DataFrame: DataFrame containing the extracted data,
                     or None if extraction fails
    """
    try:
        service = connect_to_sheets()
        
        spreadsheet_id = '15FMeidgU2Dg7Q4JKPkLAdJmQ3IxWCWJXjhCo9UterCE'
        range_name = 'Sheet1!A:Z'
        
        sheet = service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=spreadsheet_id,
            range=range_name
        ).execute()
        
        values = result.get('values', [])
        
        if not values:
            print('No data found.')
            return None
            
        df_data = pd.DataFrame(values[1:], columns=values[0])
        
        required_columns = [
            'Email address',
            'Tool used',
            'Feature Used',
            'Context Awareness',
            'Autonomy',
            'Experience',
            'Output Quality',
            'Overall Rating',
            'Unique ID',
            'Pod'
        ]
        
        return df_data[required_columns]
        
    except Exception as error:
        print(f"An error occurred: {str(error)}")
        return None

def main():
    """Main function to execute the data extraction process."""
    data = extract_sheet_data()
    
    if data is not None:
        print("Data extracted successfully!")
        print(f"Number of rows extracted: {len(data)}")
        print("\nFirst few rows of the data:")
        print(data.head())

if __name__ == "__main__":
    main()