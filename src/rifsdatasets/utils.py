"""utils for rifsdatasets"""

from git import RemoteProgress
from awesome_progress_bar import ProgressBar


class CloneProgress(RemoteProgress):
    """Progress bar for cloning a git repository."""

    def __init__(self, total):
        """Initialize progress bar.

        Parameters
        ----------
        total : int
            Total number of operations.

        Returns
        -------
        None
        """
        super().__init__()
        self.pbar = ProgressBar(
            1, prefix="Downloading", suffix="of files", use_eta=True, spinner_type="db"
        )

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
        self.pbar()
