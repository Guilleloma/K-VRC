import os
import sys

# Añadir el directorio padre al sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from audio_controller import AudioPlayer

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    library_path = os.path.join(current_dir, '..', 'audios')
    player = AudioPlayer(library_path)

    # Reproducir diferentes archivos de audio
    player.play_audio('hi.wav')
    player.play_audio('nofun.wav')
    player.play_audio('bye.wav')

if __name__ == "__main__":
    main()
