"""
Utilities for cleaning and transforming ChEMBL bioactivity data.

This module provides functions for converting data types,
filtering bioactivity records, and preparing datasets for
downstream analyses.
"""

import pandas as pd


NUMERIC_COLUMNS = {
    "standard_value": float,
    "pchembl_value": float,
    "value": float,
    "upper_value": float,
    "document_year": "Int64",
}

POTENCY_ACTIVITY_TYPES = [
    "IC50",
    "Ki",
    "Kd",
    "EC50",
]


def convert_numeric_columns(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
Convert selected ChEMBL columns to appropriate
numeric pandas data types while preserving missing values.

Parameters
----------
df : pandas.DataFrame
    DataFrame containing raw ChEMBL bioactivity records.

Returns
-------
pandas.DataFrame
    Copy of the input DataFrame with selected columns
    converted to numeric data types.
"""
    clean_df = df.copy()

    for column, dtype in NUMERIC_COLUMNS.items():
        clean_df[column] = pd.to_numeric(
            clean_df[column],
            errors="coerce"
        )

        if dtype == "Int64":
            clean_df[column] = clean_df[column].astype("Int64")

    return clean_df


def filter_standardized(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
Keep only standardized bioactivity records.

Parameters
----------
df : pandas.DataFrame
    DataFrame containing ChEMBL bioactivity records.

Returns
-------
pandas.DataFrame
    Copy of the input DataFrame containing only
    standardized bioactivity measurements.
"""
    clean_df = df.copy()

    clean_df = clean_df[
        clean_df["standard_flag"] == 1
    ].reset_index(drop=True)

    return clean_df


def filter_activity_types(
    df: pd.DataFrame,
    activity_types: list[str] = POTENCY_ACTIVITY_TYPES
) -> pd.DataFrame:
    """
Keep only quantitative potency and affinity measurements.

Parameters
----------
df : pandas.DataFrame
    DataFrame containing ChEMBL bioactivity records.

Returns
-------
pandas.DataFrame
    Copy of the input DataFrame containing only
    selected potency-related activity types.
"""
    clean_df = df.copy()

    clean_df = clean_df[
        clean_df["standard_type"].isin(POTENCY_ACTIVITY_TYPES)
    ]

    clean_df = clean_df[
        clean_df["standard_type"].isin(activity_types)
    ].reset_index(drop=True)

    return clean_df
