"""
This module contains the Danpass dataset.
"""

from rifsdatasets.base import Base


class CommonVoiceDansk(Base):
    """
    Dataset for the DanPASS dataset.
    """

    @staticmethod
    def download(target_folder: str, verbose: bool = False, quiet: bool = False):
        """
        Download the dataset to the specified destination.

        Parameters
        ----------
        target_folder: str
            The destination folder to download the dataset to.
        verbose: bool
            Whether to print the download progress with steps.
        quiet: bool
            Prints nothing.

        Returns
        -------
        None

        """
        from tempfile import TemporaryDirectory
        from rifsdatasets.utils import CloneProgress
        from git import Repo
        from shutil import move

        import os
        from os.path import join

        target = join(target_folder, "CommonVoiceDansk")
        if verbose and not quiet:
            print(f"Downloading CommonVoiceDansk to '{target_folder}'")
        if os.path.exists(target):
            if verbose and not quiet:
                print(
                    f"Skipping download because {target} already exists.",
                    "Review and delete the folder if you want to download again.",
                    sep="\n",
                )
            return

        with TemporaryDirectory() as tmpdirname:
            if verbose and not quiet:
                print("Created temporary directory", tmpdirname)
            Repo.clone_from(
                url="git@github.com:rifs-is-free-speech/CommonVoiceDansk.git",
                to_path=tmpdirname,
                progress=None if quiet else CloneProgress(),
            )
            if verbose and not quiet:
                print("Download complete!")

            os.makedirs(target, exist_ok=True)
            if verbose and not quiet:
                print(f"Created folder '{target}'")
            move(join(tmpdirname, "all.csv"), f"{target}/all.csv")
            move(join(tmpdirname, "train.csv"), f"{target}/train.csv")
            move(join(tmpdirname, "dev.csv"), f"{target}/dev.csv")
            move(join(tmpdirname, "test.csv"), f"{target}/test.csv")
            move(join(tmpdirname, "cleaning.py"), f"{target}/cleaning.py")
            if verbose and not quiet:
                print(f"Moved csv files to '{target}'")
            move(join(tmpdirname, "audio"), f"{target}/audio")
            if verbose and not quiet:
                print(f"Moved audio/ to '{target}'")

            if not quiet:
                print(
                    """Warning: CommonVoiceDansk is a private dataset. You
                need to request access to the dataset from the authors. When
                you have downloaded the data, then place it in the audio
                folder. We suggest that you read more about the datasets in the
                documentation."""
                )
