from biobb_vs.fpocket.fpocket_run import fpocket_run
import sys

if __name__ == "__main__":
    with open(snakemake.log[0], "w") as f:
        sys.stderr = sys.stdout = f


        prop = {
            'min_radius': 3,
            'max_radius': 6,
            'num_spheres': 35,
            'sort_by': 'druggability_score'
        }
        fpocket_run(input_pdb_path='conservative/protein.pdb',
                    output_pockets_zip='fpocket/Pockets.zip',
                    output_summary='fpocket/Summary.json',
                    properties=prop)
