"""
Utilities for calculating molecular descriptors from
chemical structures.

This module provides functions for computing
physicochemical descriptors used in cheminformatics
analyses.
"""

# Imports
import pandas as pd

from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.Chem import Crippen
from rdkit.Chem import Lipinski
from rdkit.Chem import rdFingerprintGenerator
from rdkit.Chem.Scaffolds import MurckoScaffold

# Configuration
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


# Private helpers
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


# Public functions
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


def calculate_morgan_fingerprints(
    molecules: pd.DataFrame,
    radius: int = 2,
    n_bits: int = 2048
) -> pd.DataFrame:
    """
    Calculate Morgan fingerprints for a molecule dataset.

    Parameters
    ----------
    molecules : pandas.DataFrame
        Molecule-level dataset containing canonical SMILES.

    radius : int, default=2
        Radius used to generate Morgan fingerprints.

    n_bits : int, default=2048
        Length of the fingerprint bit vector.

    Returns
    -------
    pandas.DataFrame
        Copy of the input DataFrame enriched with Morgan
        fingerprints.
    """

    generator = rdFingerprintGenerator.GetMorganGenerator(
        radius=radius,
        fpSize=n_bits,
    )

    fingerprint_df = molecules.copy()

    fingerprints = []

    for smiles in fingerprint_df["canonical_smiles"]:

        mol = _smiles_to_mol(smiles)

        fingerprint = generator.GetFingerprint(mol)

        fingerprints.append(fingerprint)

    fingerprint_df["morgan_fingerprint"] = fingerprints

    return fingerprint_df


def calculate_murcko_scaffolds(
    molecules: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculate Bemis–Murcko scaffolds for a molecule dataset.

    Parameters
    ----------
    molecules : pandas.DataFrame
        Molecule-level dataset containing canonical SMILES.

    Returns
    -------
    pandas.DataFrame
        Copy of the input DataFrame enriched with Murcko
        scaffold SMILES.
    """

    scaffold_df = molecules.copy()

    scaffolds = []

    for smiles in scaffold_df["canonical_smiles"]:

        mol = _smiles_to_mol(smiles)

        scaffold = MurckoScaffold.GetScaffoldForMol(mol)

        scaffold_smiles = Chem.MolToSmiles(scaffold)

        scaffolds.append(scaffold_smiles)

    scaffold_df["murcko_scaffold"] = scaffolds

    return scaffold_df
