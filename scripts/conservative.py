from prody import parseMSA, calcShannonEntropy, parsePDB, writePDB
from get_data_from_summary import get_best_protein
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
import numpy as np
import pandas as pd
from os import makedirs, system
from random import sample
import sys

def plot_cons(ent, ind, dom):
    a4_dims = (40, 8.27)
    n = len(dom[0]) + 1
    colors = sample(list(mcolors.CSS4_COLORS.keys()), n)
    fig, ax = plt.subplots(figsize=a4_dims)
    sns.set(style="whitegrid", color_codes=True)
    df = pd.DataFrame(
        {'x_axis': ind,
         'y_axis': ent
         })

    df["Label"] = "No Domain"
    palette = {}
    for i, domain in enumerate(dom[0]):
        palette[i+1] = colors[i+1]
        for dist in domain:
            df.loc[dist[0]:dist[1], "Label"] = i+1

    palette['No Domain'] = colors[0]

    ax.legend()
    bar_plot = sns.barplot(data=df, x="x_axis", y="y_axis", hue="Label", palette=palette, dodge=False, ax=ax)
    fig = bar_plot.get_figure()
    fig.savefig("conservative/plot.png")


def render_pymol():
    system('pymol -cq scripts/pymol_cons.pml')


if __name__ == "__main__":
    with open(snakemake.log[0], "w") as f:
        sys.stderr = sys.stdout = f

        pdb, domains = get_best_protein()

        msa = parseMSA('msa/msa.fasta')
        pdb_seq = parsePDB(pdb)

        entropy = calcShannonEntropy(msa)

        indices = pdb_seq.ca.getResnums()

        selprot = pdb_seq.copy()
        resindex = selprot.getResindices()
        entropy_prot = [entropy[ind] for ind in resindex]
        selprot.setBetas(entropy_prot)

        makedirs('conservative')
        plot_cons(entropy, indices, domains)
        writePDB('conservative/protein.pdb', selprot)
        render_pymol()
