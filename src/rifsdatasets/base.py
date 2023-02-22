"""
Base class for all datasets.
"""

from abc import ABC, abstractmethod


class Base(ABC):
    """
    Base class for all datasets.
    """

    @staticmethod
    @abstractmethod
    def download(target_folder: str, verbose: bool = False):
        """
        Download the dataset to the specified destination.

        Parameters
        ----------
        target_folder: str
            The destination folder to download the dataset to.
        verbose: bool
            Whether to print the download progress.
        """
        ...
