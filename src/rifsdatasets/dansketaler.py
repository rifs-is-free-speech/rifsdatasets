"""
This module contains the DanskeTaler dataset.
"""

from rifsdatasets.base import Base


class DanskeTaler(Base):
    """
    Dataset for the DanskeTaler dataset.
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
        import os
        from os.path import join

        import pandas as pd

        from rifsdatasets.utils import CloneProgress, convert_mp3_to_wav

        from git import Repo
        from shutil import move
        from tempfile import TemporaryDirectory

        target = join(target_folder, "DanskeTaler")
        if verbose and not quiet:
            print(f"Downloading DanskeTaler to '{target_folder}'")
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
                url="git@github.com:rifs-is-free-speech/DanskeTaler.git",
                to_path=tmpdirname,
                progress=None if quiet else CloneProgress(),
            )
            if verbose and not quiet:
                print("Download complete!")
                print("Converting mp3 to wav")

            # Convert mp3 files to wav
            os.mkdir(join(tmpdirname, "audio_wav"))
            all_csv = pd.read_csv(join(tmpdirname, "all.csv"))
            for i, row in all_csv.iterrows():
                if verbose and not quiet:
                    print(f"Converting {row['id']}")
                convert_mp3_to_wav(
                    src=join(tmpdirname, "audio", f"{row['id']}.mp3"),
                    dst=join(tmpdirname, "audio_wav", f"{row['id']}.wav"),
                )

            os.makedirs(target, exist_ok=True)
            if verbose and not quiet:
                print(f"Created folder '{target}'")
            move(join(tmpdirname, "all.csv"), f"{target}/all.csv")
            if verbose and not quiet:
                print(f"Moved all.csv to '{target}'")
            move(join(tmpdirname, "text"), f"{target}/text")
            if verbose and not quiet:
                print(f"Moved text/ to '{target}'")
            move(join(tmpdirname, "audio_wav"), f"{target}/audio")
            if verbose and not quiet:
                print(f"Moved audio/ to '{target}'")
