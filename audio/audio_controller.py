import os
from pydub import AudioSegment
from pydub.playback import play

class AudioPlayer:
    def __init__(self, library_path=None):
        """
        Si no se indica library_path, se utiliza la carpeta 'audios' que está
        dentro de la carpeta 'audio' (que es donde se encuentra este archivo).
        """
        if library_path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            library_path = os.path.join(base_dir, "audios")
        self.library_path = os.path.abspath(library_path)
        
        # Creamos la carpeta si no existe
        if not os.path.exists(self.library_path):
            os.makedirs(self.library_path)
            print(f"[DEBUG] Se creó el directorio de audio: {self.library_path}")

    def play_audio(self, file_name):
        """
        Reproduce el archivo de audio (en formato WAV) que se encuentre en self.library_path.
        """
        file_path = os.path.join(self.library_path, file_name)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"El archivo '{file_name}' no se encuentra en {self.library_path}")
        
        audio = AudioSegment.from_wav(file_path)
        play(audio)

if __name__ == "__main__":
    # Ejemplo de uso: se intenta reproducir 'hi.wav' de la carpeta 'audios'
    player = AudioPlayer()
    try:
        player.play_audio("hi.wav")
    except Exception as e:
        print(f"Error: {e}")
