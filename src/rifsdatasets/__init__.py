"""
Package for downloading and loading the rifs datasets
"""

from rifsdatasets.librivox import LibriVoxDansk
from rifsdatasets.den2radio import Den2Radio
from rifsdatasets.forskerzonen import Forskerzonen
from rifsdatasets.merge_rifsdatasets import merge_rifsdatasets

__version__ = "0.1.3"

all_datasets = {
    "LibriVoxDansk": LibriVoxDansk,
    "Den2Radio": Den2Radio,
    "Forskerzonen": Forskerzonen,
}

__all__ = ["all_datasets", "merge_rifsdatasets"]
