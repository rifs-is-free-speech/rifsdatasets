"""
This module can download noisepacks from freesound.org.
"""

from sklearn.model_selection import train_test_split

from rifsdatasets.base import Base

import requests as re
import zipfile
import os


class FreeSoundOrg(Base):
    """
    Dataset for the FreeSoundOrg noisepacks.
    """

    @staticmethod
    def download(
        target_folder: str,
        pack_id: int,
        name: str = "",
        verbose: bool = False,
        quiet: bool = False,
    ):
        """
        Download the dataset to the specified destination.

        Parameters
        ----------
        target_folder: str
            The destination folder to download the dataset to.
        pack_id: int
            The id of the noisepack to download.
        name: str
            The name of the noisepack. Optional. Defaults to the freesound pack name.
        verbose: bool
            Whether to print the download progress with steps.
        quiet: bool
            Prints nothing.

        Returns
        -------
        None

        """

        # TODO: Get from environment variables or settings file
        token = ""
        oauth2_token = ""

        base_url = "https://freesound.org"
        headers = {"Authorization": f"Token {token}"}
        headers_oauth2 = {"Authorization": f"Bearer {oauth2_token}"}

        if not name:
            if verbose and not quiet:
                print("No name supplied, getting name of soundpack")
            response = re.get(f"{base_url}/apiv2/packs/{pack_id}/", headers=headers)
            assert response.status_code == 200, "Could not get pack name"
            name = response.json()["name"]
            name = "".join(
                [c for c in name.lower() if c.isalnum() or c == " "]
            ).rstrip()

        if verbose and not quiet:
            print(f"Name of soundpack: {name}")

        os.makedirs(os.path.join(target_folder, name, "audio"), exist_ok=True)

        if verbose and not quiet:
            print("Downloading sounds into zip")
        pack_url = f"{base_url}/apiv2/packs/{pack_id}/download/"
        filepath = os.path.join(target_folder, name, f"{name}.zip")
        with re.get(pack_url, headers=headers_oauth2, stream=True) as r:
            r.raise_for_status()
            with open(filepath, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        if verbose and not quiet:
            print("Unzipping")
        with zipfile.ZipFile(filepath, "r") as zip_ref:
            zip_ref.extractall(os.path.join(target_folder, name, "audio"))

        print("Removing zip")
        os.remove(filepath)

        if verbose and not quiet:
            print("Getting sounds and splitting dataset")
        sounds = [
            s
            for s in os.listdir(os.path.join(target_folder, name, "audio"))
            if s.endswith(".wav")
        ]

        # Split dataset
        train, rest = train_test_split(sounds, train_size=0.7)
        dev, test = train_test_split(rest, train_size=0.5)

        # Write splits to txt
        if verbose and not quiet:
            print("Writing splits to txt")
        for txtname, dataset in [
            ("train.txt", train),
            ("dev.txt", dev),
            ("test.txt", test),
        ]:
            with open(os.path.join(target_folder, name, txtname), "w") as f:
                for line in dataset:
                    f.write(f"{line}\n")

        if verbose and not quiet:
            print("Done")
