# config.py
# Variables globales de configuración para la aplicación

SILENCE_THRESHOLD = 30      # Valor de RMS para considerar silencio (ajústalo según tus pruebas)
CHANNELS = 1                 # Número de canales (1 = mono, 2 = estéreo, etc.)
RATE = 16000                 # Frecuencia de muestreo (Hz)
CHUNK = 1024                 # Tamaño de cada bloque de audio
SILENCE_DURATION = 2.0       # Segundos de silencio consecutivos para detener la grabación
TEMP_AUDIO_PATH = "temp_audio.wav"  # Ruta por defecto para guardar el audio temporal

# Configuración específica de PyAudio
AUDIO_FORMAT = 'int16'     # Formato de audio
DEVICE_INDEX = None        # None usa el dispositivo por defecto, cambiar si es necesario

# Configuración de hardware - GPIO
LED_PIN = 27               # Pin GPIO para el LED principal
# BUTTON_PIN = 17          # Pin GPIO para el botón (descomentar si se implementa)
# SERVO_PIN = 18           # Pin GPIO para servo de movimiento (descomentar si se implementa)

# Agrega otras variables globales:
