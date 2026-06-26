"""
Client for interacting with the ChEMBL REST API.

This module provides low-level methods for sending requests to the
ChEMBL API and retrieving paginated resources.
"""

import requests


class ChEMBLClient:
    """
Client for interacting with the ChEMBL REST API.

Provides methods for retrieving individual API responses and
automatically downloading paginated resources.
"""

    BASE_URL = "https://www.ebi.ac.uk/chembl/api/data"

    def __init__(self):

        pass

    def get(self, endpoint, params=None):
        """
Send a GET request to a ChEMBL API endpoint.

This method retrieves a single response page from the API.

Parameters
----------
endpoint : str
    API endpoint (e.g. "target/search").

params : dict, optional
    Query parameters.

Returns
-------
dict
    JSON response returned by the ChEMBL API.
"""
        url = f"{self.BASE_URL}/{endpoint}"
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_all(
        self,
        endpoint: str,
        response_key: str,
        params: dict | None = None,
        page_size: int = 1000,
        show_progress: bool = False
    ) -> list[dict]:
        """
Retrieve all records from a paginated ChEMBL endpoint.

The method automatically requests successive pages until all
available records have been downloaded and returns them as a
single list.

Parameters
----------
endpoint : str
    ChEMBL API endpoint.

response_key : str
    Name of the key containing the records in the API response
    (e.g. "activities", "molecules", "targets").

params : dict, optional
    Query parameters used in every request.

page_size : int, default=1000
    Number of records requested per page.

show_progress : bool, default=False
    Shows progress bar.

Returns
-------
list[dict]
    List containing all records returned by the endpoint.
"""

        if params is None:
            params = {}

        all_records = []

        offset = 0

        total_count = None

        while total_count is None or offset < total_count:

            request_params = {
                **params,
                "limit": page_size,
                "offset": offset,
                "format": "json"
            }

            response = self.get(
                endpoint=endpoint,
                params=request_params
            )

            total_count = response["page_meta"]["total_count"]

            all_records.extend(response[response_key])

            offset += page_size

            if show_progress:
                downloaded = min(offset, total_count)

                progress = downloaded / total_count

                percentage = progress * 100

                bar_length = 30

                filled = int(progress * bar_length)

                bar = "█" * filled + "-" * (bar_length - filled)

                print(
                    f"\r[{bar}] {downloaded:,}/{total_count:,}",
                    end="",
                    flush=True
                )

        if show_progress:
            print(f"({percentage:.1f}%)")

        return all_records
