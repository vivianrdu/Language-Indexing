from abc import ABC, abstractmethod
import requests
import urllib.parse


class IAirtableHttpClient(ABC):
    """
    Airtable Http Client Interface

    Args:
        ABC
    """

    @abstractmethod
    def list_records(self, page_size=100, offset=None, max_records=None):
        """
        List records

        Args:
            page_size (int, optional): Page size. Defaults to 100.
            offset (str, optional): Offset for pagination. Defaults to None.
            max_records (int, optional): Max records. Defaults to None.
        """
        pass

    @abstractmethod
    def get_record(self, id):
        """
        Get record

        Args:
            id (str): Id of record
        """
        pass

    @abstractmethod
    def create_record(self, fields):
        """
        Create record

        Args:
            fields (dict): Dictionary of fields
        """
        pass


class AirtableHttpClient(IAirtableHttpClient):
    """
    Http client for accessing an Airtable base

    Args:
        IAirtableHttpClient
    """

    _base_url = 'https://api.airtable.com/v0'

    def __init__(self, connection_info, table_info):
        """
        Construct AirtableHttpClient

        Args:
            connection_info (AirtableConnectionInfo)
            table_info (AirtableTableInfo)
        """

        self._route = '/'.join([
            self._base_url,
            connection_info.base_id,
            table_info.name
        ])

        self._headers = {
            'Authorization': f'Bearer {connection_info.api_key}'
        }

        self._id_column = table_info.id_column

    def list_records(self, page_size=100, offset=None, max_records=None):
        """
        List records

        Args:
            page_size (int, optional): Page size. Defaults to 100.
            offset (str, optional): Offset for pagination. Defaults to None.
            max_records (int, optional): Max records. Defaults to None.

        Returns:
            Response: Response from Airtable API
        """

        params = [
            f'maxRecords={max_records}'
        ]

        if page_size is not None:
            params.append(f'pageSize={page_size}')

        if offset is not None:
            params.append(f'offset={offset}')

        url = f'{self._route}?{"&".join(params)}'

        return requests.get(url, headers=self._headers)

    def get_record(self, id):
        """
        Get record

        Args:
            id (str): Id of record

        Returns:
            Response: Response from Airtable API
        """

        formula = urllib.parse.quote_plus(f'{{{self._id_column}}} = \'{id}\'')
        url = f'{self._route}?filterByFormula={formula}'

        return requests.get(url, headers=self._headers)

    def create_record(self, fields):
        """Create record

        Args:
            fields (dict): Dictionary of fields

        Returns:
            Response: Response from Airtable API
        """

        json_obj = {
            'records': [
                {
                    'fields': fields
                }
            ]
        }

        headers = {
            **self._headers,
            'Content-Type': 'application/json'
        }

        return requests.post(self._route, json=json_obj, headers=headers)
