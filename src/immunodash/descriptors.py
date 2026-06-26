"""
Utilities for calculating molecular descriptors from
chemical structures.

This module provides functions for computing
physicochemical descriptors used in cheminformatics
analyses.
"""

import pandas as pd

from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.Chem import Crippen
from rdkit.Chem import Lipinski

RDKIT_DESCRIPTORS = {
    "molecular_weight": Descriptors.MolWt,
    "logp": Crippen.MolLogP,
    "tpsa": Descriptors.TPSA,
    "hba": Lipinski.NumHAcceptors,
    "hbd": Lipinski.NumHDonors,
    "rotatable_bonds": Lipinski.NumRotatableBonds,
    "ring_count": Lipinski.RingCount,
    "aromatic_ring_count": Lipinski.NumAromaticRings,
}


def _smiles_to_mol(
    smiles: str
):
    """
Convert a SMILES string into an RDKit molecule.

Parameters
----------
smiles : str
    Canonical SMILES representation of a molecule.

Returns
-------
rdkit.Chem.rdchem.Mol
    RDKit molecule object.

Raises
------
ValueError
    If the SMILES string cannot be parsed.
"""
    mol = Chem.MolFromSmiles(smiles)

    if mol is None:
        raise ValueError(
            f"Invalid SMILES: '{smiles}'."
        )
    return mol


def calculate_rdkit_descriptors(
    molecules: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculate RDKit molecular descriptors.

    Parameters
    ----------
    molecules : pandas.DataFrame
        Molecule-level dataset containing canonical SMILES.

    Returns
    -------
    pandas.DataFrame
        Copy of the input DataFrame enriched with RDKit
        molecular descriptors.
    """

    descriptor_df = molecules.copy()

    descriptor_records = []

    for smiles in descriptor_df["canonical_smiles"]:

        mol = _smiles_to_mol(smiles)

        molecule_descriptors = {}

        for (
            descriptor_name,
            descriptor_function
        ) in RDKIT_DESCRIPTORS.items():

            molecule_descriptors[descriptor_name] = (
                descriptor_function(mol)
            )

        descriptor_records.append(molecule_descriptors)

    descriptor_matrix = pd.DataFrame(descriptor_records)

    descriptor_df = pd.concat(
        [descriptor_df, descriptor_matrix],
        axis=1
    )

    return descriptor_df
