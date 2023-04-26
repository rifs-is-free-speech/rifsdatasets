"""
This module contains the function to merge two datasets.
"""
from typing import List
import subprocess as sp
import pandas as pd
import os

def merge_rifsdatasets(src_dataset: List[str], trg_dataset: str, specify_dirs: List[str], verbose: bool = False, quiet: bool = False):
    """
    Merge two or more datasets.

    Parameters
    ----------
    src_dataset: List[str]
        List of datasets to merge. Should be fully qualified paths.
    trg_dataset: str
        Path to new dataset to merge. Should be fully qualified path.
    specify_dirs: List[str]
        List of directories to merge. If None, all directories will be merged. Optional.
    verbose: bool
        Whether to print the download progress with steps.
    quiet: bool
        Prints nothing.

    Returns
    -------
    None
    """

    os.makedirs(trg_dataset, exist_ok=True)

    all_csv = []

    for dataset in src_dataset:
        if verbose and not quiet:
            print(f"Merging {dataset} into {trg_dataset}")

        try:
            csv = pd.read_csv(os.path.join(dataset, "all.csv"))
            all_csv.append(csv)
        except FileNotFoundError:
            pass

        if specify_dirs:
            cmd = f"cp -r {' '.join([os.path.join(dataset, d) for d in specify_dirs])} {trg_dataset}"
        else:
            cmd = f"cp -r {dataset}/* {trg_dataset}"

        sp.Popen(cmd, shell=True).wait()

        if not quiet:
            print(f"Finished merging {dataset} into {trg_dataset}")

    if len(all_csv) > 0:
        all_csv = pd.concat(all_csv, ignore_index=True)
        all_csv.to_csv(os.path.join(trg_dataset, "all.csv"), index=False)