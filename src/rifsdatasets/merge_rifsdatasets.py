"""
This module contains the function to merge two datasets.
"""

from typing import List


def merge_rifsdatasets(
    src_dataset: List[str],
    trg_dataset: str,
    specify_dirs: List[str],
    verbose: bool = False,
    quiet: bool = False,
):
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

    import subprocess as sp
    import pandas as pd
    import os
    from collections import defaultdict

    if not specify_dirs:
        specify_dirs = ["audio", "text", "alignments"]

    os.makedirs(trg_dataset, exist_ok=True)
    csvdict = defaultdict(list)
    for dataset in src_dataset:
        dataset_name = os.path.basename(os.path.normpath(dataset))

        if verbose and not quiet:
            print(f"Merging {dataset} into {trg_dataset}")

        for split in ["train.csv", "valid.csv", "test.csv"]:
            try:
                csv = pd.read_csv(os.path.join(dataset, split))
            except FileNotFoundError:
                if verbose and not quiet:
                    print(f"Dataset {dataset} has no '{split}' split.")
                continue

            if "id" in csv.columns:
                csv["id"] = csv["id"].apply(
                    lambda x: os.path.join(
                        str(x).split("/")[0],
                        dataset_name,
                        "/".join(str(x).split("/")[1:]),
                    )
                )
            else:
                if verbose and not quiet:
                    print(
                        f"Dataset {dataset} has no 'id' column. Will only merge files but not csv."
                    )
                continue

            csvdict[split].append(csv)
        skip_all = False
        try:
            allcsv = pd.read_csv(os.path.join(dataset, "all.csv"))
            allcsv["id"] = allcsv["id"].apply(
                lambda x: os.path.join(dataset_name, str(x))
            )
            csvdict["all.csv"].append(allcsv)
        except FileNotFoundError:
            skip_all = True
            pass

        for dir in specify_dirs:
            dir_target = os.path.join(trg_dataset, dir, dataset_name)
            if not os.path.exists(os.path.join(dataset, dir)):
                continue
            os.makedirs(dir_target, exist_ok=True)
            if verbose and not quiet:
                print(f"Copying {dir} from '{dataset}' to '{trg_dataset}'")
            sp.run(
                f"cp -R {os.path.join(dataset, dir)}/* {dir_target}",
                shell=True,
                check=True,
            )

        if not quiet:
            print(f"Finished merging '{dataset}' into '{trg_dataset}'\n")

    if not quiet:
        print("Merging csv files...")
    for split in ["train.csv", "valid.csv", "test.csv"]:
        csv = pd.concat(csvdict[split])
        csv = csv.sample(frac=1).reset_index(drop=True)
        csv.to_csv(os.path.join(trg_dataset, split), index=False)

    if not quiet:
        print("creating all.csv")
    if not skip_all:
        allcsv = pd.concat(csvdict["all.csv"])
        allcsv = allcsv.sample(frac=1).reset_index(drop=True)
        allcsv.to_csv(os.path.join(trg_dataset, "all.csv"), index=False)
