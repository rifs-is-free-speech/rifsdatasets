"""
This module contains the LibriVoxDansk dataset.
"""
from tempfile import TemporaryDirectory

from rifsdatasets.base import Base
from git import Repo
from shutil import move

import os
from os.path import join


class LibriVoxDansk(Base):
    """
    Dataset for the LibriVoxDansk dataset.
    """

    @staticmethod
    def download(target_folder: str, verbose: bool = False):
        """
        Download the dataset to the specified destination.

        Parameters
        ----------
        target_folder: str
            The destination folder to download the dataset to.
        verbose: bool
            Whether to print the download progress.

        Returns
        -------
        None

        """
        if verbose:
            print(f"Downloading LibriVoxDansk to '{target_folder}'")
        with TemporaryDirectory() as tmpdirname:
            if verbose:
                print("Created temporary directory", tmpdirname)
            Repo.clone_from(
                "git@github.com:rifs-is-free-speech/LibriVoxDansk.git", tmpdirname
            )
            if verbose:
                print("Cloned repo")
            target = join(target_folder, "LibriVoxDansk")
            os.makedirs(target, exist_ok=True)
            if verbose:
                print(f"Created folder '{target}'")

            move(join(tmpdirname, "all.csv"), f"{target}/all.csv")
            if verbose:
                print(f"Moved all.csv to '{target}'")
            move(join(tmpdirname, "text"), f"{target}/text")
            if verbose:
                print(f"Moved text/ to '{target}'")
            move(join(tmpdirname, "audio"), f"{target}/audio")
            if verbose:
                print(f"Moved audio/ to '{target}'")
