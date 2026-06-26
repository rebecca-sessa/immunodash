import requests


class ChEMBLClient:
    """

    Simple client for interacting with the ChEMBL REST API.

    """

    BASE_URL = "https://www.ebi.ac.uk/chembl/api/data"

    def __init__(self):

        pass

    def get(self, endpoint, params=None):
        """

        Send a GET request to the ChEMBL API.

        Parameters

        ----------

        endpoint : str

            API endpoint (e.g. "target/search").

        params : dict, optional

            Query parameters.

        Returns

        -------

        dict

            JSON response from the API.

        """
        url = f"{self.BASE_URL}/{endpoint}"
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def _get_all(
        self,
        endpoint: str,
        params: dict | None = None,
        page_size: int = 1000
    ) -> list:
        """
        Retrieve all records from a paginated ChEMBL endpoint.
        """

        if params is None:
            params = {}

        all_records = []

        offset = 0
