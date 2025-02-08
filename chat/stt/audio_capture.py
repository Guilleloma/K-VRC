# audio_capture.py

import pyaudio
import wave
import numpy as np
from config import SILENCE_THRESHOLD, CHANNELS, RATE, CHUNK, SILENCE_DURATION, TEMP_AUDIO_PATH

class RealTimeAudioCapture:
    def __init__(self,
                 channels=CHANNELS,
                 rate=RATE,
                 chunk=CHUNK,
                 silence_threshold=SILENCE_THRESHOLD,
                 silence_duration=SILENCE_DURATION,
                 output_path=TEMP_AUDIO_PATH):
        """
        :param channels: 1 = mono, 2 = stereo, etc.
        :param rate: Frecuencia de muestreo (16k, 44.1k, etc.)
        :param chunk: Tamaño de cada bloque de audio.
        :param silence_threshold: RMS por debajo del cual consideramos 'silencio'.
        :param silence_duration: Segundos consecutivos de silencio para terminar la grabación.
        :param output_path: Archivo WAV temporal.
        """
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration
        self.output_path = output_path

        # Número de chunks consecutivos que representan 'silence_duration'
        self.silence_chunks = int((self.rate / self.chunk) * self.silence_duration)

    def _rms(self, data_bytes):
        """Calcula el RMS de un chunk de audio (16-bit). Maneja posibles NaN."""
        data_int = np.frombuffer(data_bytes, dtype=np.int16)

        if len(data_int) == 0:
            # Evitamos Mean of empty slice → NaN
            return 0.0

        rms_val = np.sqrt(np.mean(data_int.astype(np.float64) ** 2))
        if np.isnan(rms_val):
            return 0.0  # Si sale NaN, lo tomamos como 0 o lo que decidas

        return rms_val

    def listen_and_record(self):
        """
        Graba hasta que detecta 'silence_duration' segundos de silencio (según 'silence_threshold').
        Guarda el WAV en 'output_path' y retorna la ruta.
        """
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=self.channels,
                        rate=self.rate,
                        input=True,
                        frames_per_buffer=self.chunk)

        print("Comenzando a grabar. Habla por el micrófono...")

        frames = []
        silent_chunks_count = 0
        recording_active = True

        while recording_active:
            data = stream.read(self.chunk, exception_on_overflow=False)
            frames.append(data)

            rms_val = self._rms(data)
            # Debug/log para ver qué ocurre
            print(f"RMS value: {rms_val} | silent count: {silent_chunks_count}")

            if rms_val < self.silence_threshold:
                # Incrementamos el conteo de chunks silenciosos
                silent_chunks_count += 1
            else:
                # Si hay voz, reseteamos a 0
                silent_chunks_count = 0

            # Si llegamos a la cantidad de chunks que equivalen a 'silence_duration', paramos
            if silent_chunks_count >= self.silence_chunks:
                recording_active = False

        print("Silencio detectado. Finalizando grabación...")

        # Cerrar stream y PyAudio
        stream.stop_stream()
        stream.close()
        p.terminate()

        # Guardar a WAV
        wf = wave.open(self.output_path, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()

        print(f"Audio guardado en {self.output_path}")
        return self.output_path
