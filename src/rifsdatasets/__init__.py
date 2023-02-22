"""
Package for downloading and loading the rifs datasets
"""

from rifsdatasets.librivox import LibriVoxDansk

__version__ = "0.0.1"

datasets = {"LibriVoxDansk": LibriVoxDansk}

__all__ = ["datasets"]
