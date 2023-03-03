"""
Package for downloading and loading the rifs datasets
"""

from rifsdatasets.librivox import LibriVoxDansk

__version__ = "0.0.1"

all_datasets = {"LibriVoxDansk": LibriVoxDansk}

__all__ = ["all_datasets"]
