from immunodash.client import ChEMBLClient

client = ChEMBLClient()


def _has_gene_symbol(target: dict, gene_symbol: str) -> bool:
    """
Return True if a target contains the requested gene symbol.

Parameters
----------
target : dict
    ChEMBL target record.

gene_symbol : str
    Gene symbol to search for.

Returns
-------
bool
    True if the target contains the requested gene symbol,
    otherwise False.
"""

    components = target["target_components"]

    for component in components:
        synonyms = component["target_component_synonyms"]

        for synonym in synonyms:
            if (
                synonym["syn_type"] == "GENE_SYMBOL"
                and synonym["component_synonym"].casefold() == gene_symbol.casefold()
            ):
                return True
    return False


def get_target(
    target_name: str,
    organism: str = "Homo sapiens",
    target_type: str = "SINGLE PROTEIN"
) -> dict:
    """
Retrieve a validated ChEMBL target for a given gene symbol.

The function searches the ChEMBL target database and returns the
single target matching the requested gene symbol, organism,
and target type.

Parameters
----------
target_name : str
    Gene symbol (e.g. "JAK1").

organism : str, optional
    Organism to filter targets.

target_type : str, optional
    Target type to filter.

Returns
-------
dict
    Metadata describing the validated ChEMBL target.

Raises
------
ValueError
    If no matching target is found or if multiple matching
    targets are identified.
"""
    response = client.get(
        endpoint="target/search",
        params={
            "q": target_name,
            "format": "json"
        }
    )
    targets = response["targets"]

    matching_targets = []

    for target in targets:

        if (
            target["organism"] == organism
            and target["target_type"] == target_type
            and _has_gene_symbol(target, target_name)
        ):
            matching_targets.append(target)

    n_matches = len(matching_targets)

    if n_matches == 0:
        raise ValueError(
            f"No target found matching '{target_name}' "

            f"for organism '{organism}' "

            f"and target type '{target_type}'."
        )
    elif n_matches > 1:
        raise ValueError(

            f"Multiple matching targets found for '{target_name}'."

        )
    else:
        return matching_targets[0]
