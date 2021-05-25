import os.path


class AirtableTableInfo:
    """
    Information for retrieving data from a Table on Airtable
    """

    def __init__(self, name, id_column, page_size=100, max_records=100):
        """
        Construct AirtableTableInfo

        Args:
            name (str): Table name
            id_column (str): Name of identifier column
            page_size (int, optional): Number of records returned per request
            offset (str): Offset value for pagination
            max_records (int, optional): Max records to retrieve
        """

        self.name = name
        self.id_column = id_column
        self.page_size = page_size
        self.offset = None
        if os.path.exists(os.path.expanduser('~/.language-indexing-offset')):
            file = open(os.path.expanduser('~/.language-indexing-offset'), 'r')
            self.offset = file.read()
        self.max_records = max_records
