""" Den2Radio is a Danish radio station that makes none commercial radio. It is
driven by volunteers, and its radio programs are made my hobbyists. Some have
worked in Broadcasting before. Others join to have their own radio program.
This dataset is not public and therefore you may not use it for anything if you
get access. All rights are reserved for Den2Radio and its organization.

5288 episodes
268 series
47 producers
8 themes

5328 downloadable episodes
622 not apart of a series

Series description is avg 691.3047619047619 chars long if NaN is dropped for episodes with a series.
Episode description is avg 1016.6026006977481 chars long if Nan is dropped for all episodes.

Themes:
Arkiv                      52
Klassisk musik            172
Kultur                   2277
Musik                     338
Natur                     111
Politik                   185
Samfund                  1934
Videnskab og Filosofi     219

year
2009      1
2011     22
2012    214
2013    149
2014    536
2015    479
2016    549
2017    666
2018    520
2019    560
2020    529
2021    570
2022    398
2023     95
"""

from tempfile import TemporaryDirectory

from rifsdatasets.base import Base
from rifsdatasets.utils import CloneProgress, convert_mp3_to_wav
from git import Repo
from shutil import move

import os
from os.path import join
import pandas as pd


class Den2Radio(Base):
    """
    Dataset for Den2Radio dataset.
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
        target = join(target_folder, "Den2Radio")
        if verbose and not quiet:
            print(f"Downloading Den2Radio to '{target_folder}'")
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
                url="git@github.com:rifs-is-free-speech/Den2Radio.git",
                to_path=tmpdirname,
                progress=None if quiet else CloneProgress(),
            )
            if verbose and not quiet:
                print("Cloned repo")

            df = pd.read_csv(join(tmpdirname, "all.csv"))
            print(df)
            move(join(tmpdirname, "all.csv"), target)

            if verbose and not quiet:
                print("Converting mp3 to wav")

            convert_mp3_to_wav
            """
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

            """
