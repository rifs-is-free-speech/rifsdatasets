"""Split dataset
=============

The module contains one function to split_dataset into train, validation and
test sets. Used by the rifs CLI. The functionality is used to combine segments
of alignments into one.

The module contains the following function:

    - split_dataset: Split dataset into train, validation and test sets.

"""

import os

from glob import glob


def split_dataset(
    dataset_path: str,
    split_method: str = "random",
    split_ratio: float = 0.8,
    split_test_ratio: float = 0.5,
    verbose: bool = False,
    quiet: bool = False,
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
    verbose : bool
        Print progress.
    quiet : bool
        disables output.

    Returns
    -------
    None
    """
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

    search_path = os.path.join(dataset_path, "alignments")

    print(glob(os.path.join(search_path, "**/segments.txt")))
