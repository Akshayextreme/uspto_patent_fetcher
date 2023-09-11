import unittest
from unittest.mock import Mock, patch

from app import get_uspto_link, get_api_resp

class TestUsptoApp(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()
    
    def test_get_uspto_link(self):
        actual = "https://developer.uspto.gov/ibd-api/v1/application/grants?grantFromDate=2017-01-01&grantToDate=2017-01-03&start=0&rows=100&largeTextSearchFlag=N"
        link = get_uspto_link(0, 100, '2017-01-01', '2017-01-03')
        self.assertEqual(actual, link)

    def test_get_api_resp(self):
        mock_response = {'results': [{'inventionSubjectMatterCategory': 'utility',
                        'patentApplicationNumber': 'US14585764',
                        'filingDate': '12-30-2014',
                        'mainCPCSymbolText': 'A01B63/008',
                        'furtherCPCSymbolArrayText': ['A01B71/02', 'A01C7/205'],
                        'inventorNameArrayText': ['Sauder Derek A.', 'Hodel Jeremy J.'],
                        'abstractText': [],
                        'assigneeEntityName': 'Precision Planting LLC',
                        'assigneePostalAddressText': 'Tremont, US',
                        'inventionTitle': 'Dynamic supplemental downforce control system for planter row units',
                        'filelocationURI': 'https://dh-opendata.s3.amazonaws.com/grant_pdf/grant_pdf_20170103/P20170103-20170103/09/532/496/09532496.pdf',
                        'archiveURI': 'https://bulkdata.uspto.gov/data/patent/grant/redbook/bibliographic/2017/ipgb20170103_wk01.zip',
                        'claimText': [],
                        'descriptionText': [],
                        'grantDocumentIdentifier': 'US09532496B2',
                        'grantDate': '01-03-2017',
                        'patentNumber': '09532496'}],
                        'recordTotalQuantity': 6502}
        mock_get = Mock()
        mock_get.json.return_value = mock_response
        mock_get.raise_for_status.return_value = None

        with patch("requests.get", return_value=mock_get):

            api = "https://developer.uspto.gov/ibd-api/v1/application/grants?grantFromDate=2017-01-01&grantToDate=2017-01-03&start=0&rows=100&largeTextSearchFlag=N"
            total_num, grants = get_api_resp(api)

            # Assertions
            self.assertEqual(total_num, 6502)
            self.assertEqual(
                set(grants.columns) - set(['patentNumber', 'patentApplicationNumber', 'assigneeEntityName', 'filingDate', 'grantDate', 'inventionTitle']), set())

    def test_test_get_api_error_handling(self):
        # Mock a response with an error status code
        mock_get = Mock()
        mock_get.raise_for_status.side_effect = Exception("API Error")

        # Patch the requests.get method with the mock
        with patch("requests.get", return_value=mock_get):

            # Call the get_api_resp function
            with self.assertRaises(Exception) as context:
                api = "https://example.com/api/data"
                total_num, grants = get_api_resp(api)

            # Assertions
            self.assertIn("API Error", str(context.exception))

    def test_get_patents_between_dates(self):
        '''
        This should also be tested, skipping now because lack of time!
        '''
        pass 