"""utils for rifsdatasets"""

from git import RemoteProgress
from awesome_progress_bar import ProgressBar
from time import sleep


class CloneProgress(RemoteProgress):
    """Progress bar for cloning a git repository."""

    def __init__(self):
        """Initialize progress bar.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        super().__init__()
        self.pbar = ProgressBar(
            1,
            prefix="Downloading",
            suffix="of files",
            use_eta=True,
            spinner_type="db",
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
        if self.pbar.total == 1:
            self.pbar.total = int(max_count)
        if cur_count == max_count:
            self.pbar._iteration = int(max_count)
            sleep(0.125)
            self.pbar.stop()
            self.pbar.wait()
        else:
            if message:
                self.pbar.prefix = f"{message} "
            self.pbar.iter()


def convert_mp3_to_wav(
    src: str,
    dst: str,
):
    """
    Convert mp3 to wav.

    Parameters
    ----------
    src: str
        Path to source mp3 file with extension
    dst: str
        Path to destination wav file with extension


    Returns
    -------
    None
    """
    import pydub

    sound = pydub.AudioSegment.from_mp3(src)
    sound.export(dst, format="wav")
