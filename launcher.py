import snakemake
import datetime
import psutil
import argparse
import shutil
from inspect import getsourcefile
import json
import os


def get_parser_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--snakefile",
        default="Snakefile",
        help="Snakemake file path"
    )

    parser.add_argument(
        "--id",
        help="Uniprot Protein ID"
    )

    parser.add_argument(
        "--cores",
        default=max(1, psutil.cpu_count() - 1),
        type=int,
        help="Number of CPU cores to use in this pipeline run (default %(default)s)"
    )

    parser.add_argument(
        "--memory",
        default=max(1, int(psutil.virtual_memory().total/(1024.**3))),
        type=int,
        help="Number of RAM in gb to use in this pipeline run (default %(default)s)"
    )

    parser.add_argument(
        "--real-run",
        help="If this argument is present, Snakemake will run the pipeline instead of dry-run, it is False by default",
        action="store_true"
    )

    parser.add_argument(
        "--unlock",
        help="If this argument is present, Snakemake will simply unlock working directory without launch anything, it is False by default",
        action="store_true"
    )

    parser.add_argument(
        "--directory",
        default=".",
        help="Snakemake working directory"
    )

    parser.add_argument(
        '--rule',
        default=None,
        help='Rule which will be rerun forcefully'
    )

    parser.add_argument(
        '--until',
        default=None,
        help='Rule which will be the last to run'
    )

    parser.add_argument(
        '--target',
        default=['all'],
        nargs='*',
        help='Target rules, snakemake will run only rules that lead to the input of this rules'
    )

    args = parser.parse_args()
    return args


if __name__ == '__main__':

    start_time = datetime.datetime.now()

    args = get_parser_args()

    # Create directories if necessary
    if not os.path.exists(args.directory):
        os.makedirs(args.directory)

    sample_name = os.path.split(args.id)[-1]
    sample_path = os.path.join(args.directory, sample_name)

    if not os.path.exists(sample_path):
        shutil.copy(args.input, sample_path)

    # Rewrite config according to the --flags
    current_path = os.path.dirname(getsourcefile(lambda: 0))
    with open(os.path.join(current_path, 'config.json'), 'r') as config:
        config_dict = json.load(config)
        config_dict['id'] = args.id
        config_dict['memory'] = args.memory

    # Run snakemake
    if not snakemake.snakemake(
            snakefile=args.snakefile,
            workdir=args.directory,
            cores=args.cores,
            config=config_dict,
            unlock=args.unlock,
            printshellcmds=True,
            dryrun=(not args.real_run),
            targets=args.target,
            stats='stat_file.txt',
            forcerun=[args.rule] if args.rule is not None else [],
            until=[args.until] if args.until is not None else [],
            use_conda=True,
            keepgoing=True
    ):
        raise ValueError("Pipeline failed see Snakemake error message for details")

    end_time = datetime.datetime.now()
    print("--- Pipeline running time: %s ---" % (str(end_time - start_time)))
