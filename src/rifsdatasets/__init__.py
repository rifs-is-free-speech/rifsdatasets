"""
Package for downloading and loading the rifs datasets
"""

from rifsdatasets.librivox import LibriVoxDansk
from rifsdatasets.den2radio import Den2Radio

__version__ = "0.1.1"

all_datasets = {"LibriVoxDansk": LibriVoxDansk, "Den2Radio": Den2Radio}

__all__ = ["all_datasets"]
