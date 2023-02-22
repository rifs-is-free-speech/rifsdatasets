from abc import ABC, abstractmethod

class Base(ABC):
    """
    Base class for all datasets.
    """

    @staticmethod
    @abstractmethod
    def download(target_folder: str):
        """
        Download the dataset to the specified destination.

        Parameters
        ----------
        target_folder: str
            The destination folder to download the dataset to.
        """
        ...