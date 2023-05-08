"""
Package for downloading and loading the rifs datasets
"""

from rifsdatasets.librivox import LibriVoxDansk
from rifsdatasets.den2radio import Den2Radio
from rifsdatasets.forskerzonen import Forskerzonen
from rifsdatasets.danpass import DanPass
from rifsdatasets.commonvoicedansk import CommonVoiceDansk
from rifsdatasets.merge_rifsdatasets import merge_rifsdatasets
from rifsdatasets.split_dataset import split_dataset

__version__ = "0.1.6"

all_datasets = {
    "LibriVoxDansk": LibriVoxDansk,
    "Den2Radio": Den2Radio,
    "Forskerzonen": Forskerzonen,
    "DanPASS": DanPass,
    "CommonVoiceDansk": CommonVoiceDansk,
}

__all__ = ["all_datasets", "merge_rifsdatasets", "split_dataset"]
