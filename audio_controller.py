from pydub import AudioSegment
from pydub.playback import play
import os

class AudioPlayer:
    def __init__(self, library_path):
        self.library_path = library_path

    def play_audio(self, file_name):
        file_path = os.path.join(self.library_path, file_name)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_name} not found in {self.library_path}")
        
        audio = AudioSegment.from_wav(file_path)
        play(audio)
