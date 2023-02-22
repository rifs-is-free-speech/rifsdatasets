from rifsdatasets.base import Base

class LibriSpeechDansk(Base):

    @staticmethod
    def download(target_folder: str):
        print("Downloading LibriSpeechDansk to " + target_folder)