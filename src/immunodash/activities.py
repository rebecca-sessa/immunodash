"""
Utilities for retrieving bioactivity records from ChEMBL.

This module provides functions for downloading experimental
bioactivity data associated with validated biological targets.
"""

from immunodash.client import ChEMBLClient

client = ChEMBLClient()


def get_activities(
    target: dict
) -> list[dict]:
    """
Retrieve all bioactivity records associated with a validated target.

Parameters
----------
target : dict
    Validated target dictionary returned by ``get_target()``.

Returns
-------
list[dict]
    List of bioactivity records retrieved from ChEMBL.
"""

    activities = client.get_all(
        endpoint="activity",
        response_key="activities",
        params={
            "target_chembl_id": target["target_chembl_id"]
        }
    )

    if "target_chembl_id" not in target:
        raise ValueError(
            "Target dictionary must contain 'target_chembl_id'."
        )

    return activities
