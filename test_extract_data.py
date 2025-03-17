import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from extract_data import connect_to_sheets, extract_sheet_data

class TestGoogleSheetsExtraction(unittest.TestCase):
    """Test cases for Google Sheets data extraction functionality"""

    @patch('extract_data.Credentials')
    @patch('extract_data.build')
    def test_connect_to_sheets(self, mock_build, mock_credentials):
        """Test the connection to Google Sheets"""
        # Setup mock
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        
        # Execute
        result = connect_to_sheets()
        
        # Assert
        self.assertEqual(result, mock_service)
        mock_credentials.from_service_account_file.assert_called_once()
        mock_build.assert_called_once_with('sheets', 'v4', credentials=mock_credentials.from_service_account_file.return_value)

    @patch('extract_data.connect_to_sheets')
    def test_extract_sheet_data_success(self, mock_connect):
        """Test successful data extraction"""
        # Setup mock data
        mock_service = MagicMock()
        mock_connect.return_value = mock_service
        
        mock_values = [
            ['Email address', 'Tool used', 'Feature Used', 'Context Awareness', 
             'Autonomy', 'Experience', 'Output Quality', 'Overall Rating', 'Unique ID', 'Pod'],
            ['test@email.com', 'Tool1', 'Feature1', '4', '5', '3', '4', '4', 'ID1', 'Pod1']
        ]
        
        mock_service.spreadsheets().values().get().execute.return_value = {'values': mock_values}
        
        # Execute
        result = extract_sheet_data()
        
        # Assert
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 1)  # One row of data
        self.assertEqual(len(result.columns), 10)  # All required columns present

    @patch('extract_data.connect_to_sheets')
    def test_extract_sheet_data_no_data(self, mock_connect):
        """Test when no data is found"""
        # Setup mock
        mock_service = MagicMock()
        mock_connect.return_value = mock_service
        mock_service.spreadsheets().values().get().execute.return_value = {'values': []}
        
        # Execute
        result = extract_sheet_data()
        
        # Assert
        self.assertIsNone(result)

    @patch('extract_data.connect_to_sheets')
    def test_extract_sheet_data_api_error(self, mock_connect):
        """Test handling of API errors"""
        # Setup mock to raise exception
        mock_connect.side_effect = Exception("API Error")
        
        # Execute
        result = extract_sheet_data()
        
        # Assert
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()