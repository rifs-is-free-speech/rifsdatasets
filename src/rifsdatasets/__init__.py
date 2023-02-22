"""
Package for downloading and loading the rifs datasets
"""

from rifsdatasets.librispeech import LibriSpeechDansk

__version__ = "0.0.1"

datasets = {"LibriVoxDansk": LibriSpeechDansk}

__all__ = ["datasets"]
