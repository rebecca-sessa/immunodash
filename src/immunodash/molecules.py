"""
Utilities for extracting and managing unique molecules from
ChEMBL bioactivity datasets.

This module provides functions for creating molecule-level
datasets suitable for cheminformatics analyses.
"""

import pandas as pd

MOLECULE_COLUMNS = [
    "molecule_chembl_id",
    "canonical_smiles",
]


def get_unique_molecules(
    activities: pd.DataFrame
) -> pd.DataFrame:
    """
Extract unique molecules from a cleaned activity dataset.

Parameters
----------
activities : pandas.DataFrame
    Cleaned activity dataset containing one or more
    measurements for each molecule.

Returns
-------
pandas.DataFrame
    Molecule-level dataset containing one row per unique
    chemical structure.
"""
    molecules = activities.copy()

    molecules = molecules[MOLECULE_COLUMNS]

    molecules = molecules.drop_duplicates()

    molecules = molecules.reset_index(drop=True)

    if molecules["molecule_chembl_id"].duplicated().any():
        raise ValueError(
            "Duplicate molecule identifiers found."
        )

    return molecules
