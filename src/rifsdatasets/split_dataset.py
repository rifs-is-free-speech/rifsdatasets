"""Split dataset
=============

The module contains one function to split_dataset into train, validation and
test sets. Used by the rifs CLI. The functionality is used to combine segments
of alignments into one.

The module contains the following function:

    - split_dataset: Split dataset into train, validation and test sets.

"""


def split_dataset(
    dataset_path: str,
    split_method: str = "random",
    split_ratio: float = 0.8,
    split_test_ratio: float = 0.5,
    check_for_bad_alignments: bool = False,
    verbose: bool = False,
    quiet: bool = False,
    seed: int = 0,
):
    """Split dataset into train, validation and test sets.

    Parameters
    ----------
    dataset_path : str
        Path to dataset.
    split_method : str
        Method to split dataset. Options are at the moment only: 'random'.
        Will not overlap between original long audio files.
        So either a wav file is in train, validation or test set.
    split_ratio : float
        Ratio to split dataset into train and validation / test sets.
    split_test_ratio : float
        Ratio to split between validation and test set. default is 0.5.
    check_for_bad_alignments : bool
        Check for bad alignments. Default is False.
    verbose : bool
        Print progress.
    quiet : bool
        disables output.
    seed: int
        Seed for random number generator.

    Returns
    -------
    None
    """

    import math
    import random
    import pandas as pd

    from glob import glob
    from os.path import join, relpath, dirname
    from rifsalignment import check_for_good_alignment

    assert split_method == "random", "Only random split method implemented."
    if verbose and not quiet:
        print(f"Splitting with split method: {split_method}")

    assert split_ratio >= 0 and split_ratio <= 1, "Split ratio must be between 0 and 1."
    assert (
        split_test_ratio >= 0 and split_test_ratio <= 1
    ), "Split test ratio must be between 0 and 1."

    if split_ratio == 1.0:
        if verbose and not quiet:
            print("Split ratio is 1. No validation and test set.")
    else:
        if split_test_ratio == 0:
            if verbose and not quiet:
                print("Split test ratio is 0.0 so there will be no test set.")
        elif split_test_ratio == 1.0:
            if verbose and not quiet:
                print("Split test ratio is 1.0 so there will be no validation set.")
        else:
            if verbose and not quiet:
                print(
                    f"Splitting into train, validation and test set with split ratio {split_ratio} and split test ratio {split_test_ratio}."  # noqa E501
                )

    if verbose and not quiet:
        print(f"Splitting dataset: {dataset_path}")

    search_path = join(dataset_path, "alignments")
    glob_search = join(search_path, "**/segments.csv")

    if verbose and not quiet:
        print(f"glob search string: {glob_search}")

    csv_files = glob(glob_search, recursive=True)

    if len(csv_files) == 0:
        raise Exception("No csv files found.")

    if verbose and not quiet:
        print(f"Found {len(csv_files)} csv files.")

    random.seed(seed)
    random.shuffle(csv_files)

    if split_ratio == 1.0:
        train = csv_files
        test = []
        valid = []

    elif split_test_ratio == 1.0:
        split_index = math.floor(split_ratio * len(csv_files))
        train = csv_files[:split_index]
        test = csv_files[split_index:]
        valid = []
    elif split_test_ratio == 0.0:
        split_index = math.floor(split_ratio * len(csv_files))
        train = csv_files[:split_index]
        test = []
        valid = csv_files[split_index:]

    else:
        if len(csv_files) % 2 == 0:
            split_index = math.floor(len(csv_files) * split_ratio)
            test_split_index = math.floor(
                split_index + (len(csv_files) - split_index) * split_test_ratio
            )
        else:
            split_index = math.ceil(len(csv_files) * split_ratio)
            test_split_index = math.ceil(
                split_index + (len(csv_files) - split_index) * split_test_ratio
            )

        train = csv_files[:split_index]
        test = csv_files[split_index:test_split_index]
        valid = csv_files[test_split_index:]

    splits = []

    if train:
        splits.append(("train", train))
        if verbose and not quiet:
            print(f"train: {len(train)}, ratio: {len(train)/len(csv_files)}")
    if test:
        splits.append(("test", test))
        if verbose and not quiet:
            print(f"test: {len(test)}, ratio: {len(test)/(len(csv_files)-len(train))}")
    if valid:
        splits.append(("valid", valid))
        if verbose and not quiet:
            print(
                f"valid: {len(valid)}",
                f"ratio: {len(valid)/(len(csv_files)-len(train))}",
            )

    for split in splits:
        split_name, csv_files = split
        all_segments = []
        for csv_file in csv_files:
            if verbose and not quiet:
                print(f"Reading segments from '{csv_file}'")
            try:
                df = pd.read_csv(csv_file)
            except pd.errors.EmptyDataError:
                if verbose and not quiet:
                    print(f"Empty csv file: {csv_file}")
                continue
            df["id"] = df["file"].apply(
                lambda x: join(dirname(relpath(csv_file, dataset_path)), x)
            )
            if check_for_bad_alignments:
                if verbose and not quiet:
                    print("Checking for bad alignments and removing them.")
                assert (
                    "model_output" in df.columns and "text" in df.columns
                ), "'model_output' or 'text' column not found in csv file."
                df = df[
                    df.apply(
                        lambda x: check_for_good_alignment(
                            x["text"], x["model_output"]
                        ),
                        axis=1,
                    )
                ]
            all_segments.append(df)
        all_segments = pd.concat(all_segments)
        all_segments.to_csv(join(dataset_path, f"{split_name}.csv"), index=False)
