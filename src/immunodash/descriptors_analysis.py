"""
Utilities for exploratory analysis of molecular descriptors.

This module provides functions for summarizing descriptor
distributions and relationships within molecule-level
datasets.
"""

import pandas as pd

from immunodash.descriptors import (
    RDKIT_DESCRIPTORS
)


def summarize_descriptors(
    descriptor_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Generate summary statistics for molecular descriptors.

    Parameters
    ----------
    descriptor_df : pandas.DataFrame
        Molecule-level dataset containing RDKit descriptors.

    Returns
    -------
    pandas.DataFrame
        Summary statistics for all molecular descriptor
        columns.
    """

    descriptor_columns = list(
        RDKIT_DESCRIPTORS.keys()
    )

    summary = (
        descriptor_df[descriptor_columns]
        .describe()
    )

    return summary
