"""
Package for downloading and loading the rifs datasets
"""

from rifsdatasets.librivox import LibriVoxDansk
from rifsdatasets.den2radio import Den2Radio
from rifsdatasets.forskerzonen import Forskerzonen
from rifsdatasets.merge_rifsdatasets import merge_rifsdatasets
from rifsdatasets.split_datasets import split_datasets

__version__ = "0.1.5"

all_datasets = {
    "LibriVoxDansk": LibriVoxDansk,
    "Den2Radio": Den2Radio,
    "Forskerzonen": Forskerzonen,
}

__all__ = ["all_datasets", "merge_rifsdatasets", "split_datasets"]
