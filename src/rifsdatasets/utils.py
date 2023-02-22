"""utils for rifsdatasets"""

from git import RemoteProgress
from tqdm import tqdm


class CloneProgress(RemoteProgress):
    """Progress bar for cloning a git repository."""

    def __init__(self):
        """Initialize progress bar."""
        super().__init__()
        self.pbar = tqdm()

    def update(self, op_code, cur_count, max_count=None, message=""):
        """
        Update the progress bar.

        Parameters
        ----------
        op_code : int
            Operation code.
        cur_count : int
            Current count.
        max_count : int
            Maximum count.
        message : str
            Message.
        """

        self.pbar.total = max_count
        self.pbar.n = cur_count
        self.pbar.refresh()
