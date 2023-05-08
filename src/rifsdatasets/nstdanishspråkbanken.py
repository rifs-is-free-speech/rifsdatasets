"""
This module contains the NSTDanishSpråkbanken dataset.
"""

from rifsdatasets.base import Base


class NSTDanishSpråkbanken(Base):
    """
    Dataset for the NSTDanishSpråkbanken dataset.
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
        from git import Repo
        from shutil import move
        from rifsdatasets.utils import CloneProgress

        import os
        from os.path import join

        target = join(target_folder, "NSTDanishSpråkbanken")
        if verbose and not quiet:
            print(f"Downloading NSTDanishSpråkbanken to '{target_folder}'")
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
                url="git@github.com:rifs-is-free-speech/NSTDanishSpr-kbanken.git",
                to_path=tmpdirname,
                progress=None if quiet else CloneProgress(),
            )
            if verbose and not quiet:
                print("Download complete!")

            os.makedirs(target, exist_ok=True)
            if verbose and not quiet:
                print(f"Created folder '{target}'")
            move(join(tmpdirname, "all.csv"), f"{target}/all.csv")
            if verbose and not quiet:
                print(f"Moved all.csv to '{target}'")
            move(join(tmpdirname, "text"), f"{target}/text")
            if verbose and not quiet:
                print(f"Moved text/ to '{target}'")
            move(join(tmpdirname, "audio"), f"{target}/audio")
            if verbose and not quiet:
                print(f"Moved audio/ to '{target}'")
