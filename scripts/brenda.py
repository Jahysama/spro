"""Example use case brendapy."""

from brendapy import BrendaParser
from brendapy.console import console


def human_proteins_for_ec(ec: str = "1.1.1.1") -> None:
    """Parse the human protein entries for a given EC number in BRENDA.

    Prints overview of number of proteins, protein ids, and human proteins.
    """
    brenda = BrendaParser()
    proteins = brenda.get_proteins(ec)

    console.print(f"{len(proteins)} proteins for EC {ec} in BRENDA")
    console.print(f"Protein identifier: {proteins.keys()}")
    console.print("-" * 80)
    console.print(list(proteins.values())[0])


if __name__ == "__main__":
    human_proteins_for_ec(ec="3.4.19.12")
