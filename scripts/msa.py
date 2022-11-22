from prody import fetchPfamMSA, searchPfam, MSAFile, writeMSA, parsePDB, refineMSA, parseMSA
from get_data_from_summary import get_best_protein
from os import makedirs
import sys


if __name__ == "__main__":
    with open(snakemake.log[0], "w") as f:
        sys.stderr = sys.stdout = f

        ID = snakemake.params['id']
        pdb, domains = get_best_protein()

        raw_msa = fetchPfamMSA(list(searchPfam(ID).keys())[0])

        msafobj = parseMSA(raw_msa)

        pdb_seq = parsePDB(pdb)

        msa_refine = refineMSA(msafobj, label=pdb, seqid=0.98)

        makedirs('msa')
        writeMSA('msa/msa.fasta', msa_refine)
