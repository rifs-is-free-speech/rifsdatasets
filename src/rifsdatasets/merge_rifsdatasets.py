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

    if not specify_dirs:
        specify_dirs = ["audio", "text", "alignments"]

    os.makedirs(trg_dataset, exist_ok=True)

    all_csv, train_csv, dev_csv = [], [], []

    for dataset in src_dataset:
        dataset_name = os.path.basename(os.path.normpath(dataset))

        if verbose and not quiet:
            print(f"Merging {dataset} into {trg_dataset}")

        for csv_file in ["all.csv", "train.csv", "valid.csv"]:
            try:
                csv = pd.read_csv(os.path.join(dataset, csv_file))
                if "id" in csv.columns:
                    csv["id"] = csv["id"].apply(
                        lambda x: os.path.join(dataset_name, str(x))
                    )
                    if csv_file == "all.csv":
                        all_csv.append(csv)
                    elif csv_file == "train.csv":
                        train_csv.append(csv)
                    elif csv_file == "valid.csv":
                        dev_csv.append(csv)
                else:
                    if verbose and not quiet:
                        print(
                            f"Dataset {dataset} has no 'id' column. Will only merge files but not csv."
                        )
            except FileNotFoundError:
                if verbose and not quiet:
                    print(f"Dataset {dataset} has no '{csv_file}'.")

        for dir in specify_dirs:
            dir_target = os.path.join(trg_dataset, dir, dataset_name)
            if not os.path.exists(os.path.join(dataset, dir)):
                continue
            os.makedirs(dir_target, exist_ok=True)
            if verbose and not quiet:
                print(f"Copying {dir} from '{dataset}' to '{trg_dataset}'")
            sp.run(
                f"cp -r {os.path.join(dataset, dir)} {dir_target}",
                shell=True,
                check=True,
            )

        if not quiet:
            print(f"Finished merging '{dataset}' into '{trg_dataset}'\n")

    print("Merging csv files...")
    print(f"all_csv: {len(all_csv)}")
    print(f"train_csv: {len(train_csv)}")
    print(f"dev_csv: {len(dev_csv)}")

    if len(all_csv) > 0:
        all_csv = pd.concat(all_csv, ignore_index=True)
        all_csv.to_csv(os.path.join(trg_dataset, "all.csv"), index=False)

    if len(train_csv) > 0 and len(dev_csv) > 0:
        train_csv = pd.concat(train_csv, ignore_index=True)
        train_csv.to_csv(os.path.join(trg_dataset, "train.csv"), index=False)

        dev_csv = pd.concat(dev_csv, ignore_index=True)
        dev_csv.to_csv(os.path.join(trg_dataset, "dev.csv"), index=False)
