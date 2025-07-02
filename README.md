# NeuroBridge
Creador de Módulos funcionales

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Para capturar audio con un micrófono es necesario instalar la biblioteca
PortAudio en tu sistema. En distribuciones basadas en Debian puedes hacerlo con
`apt`:

```bash
sudo apt-get install portaudio19-dev
```

En macOS usa Homebrew:

```bash
brew install portaudio
```

## Módulo de control de voz

El archivo `voice_control.py` implementa un reconocimiento de voz
**sin conexión a internet** utilizando la librería `vosk`.

Antes de ejecutarlo, descarga un modelo de voz en español desde
<https://alphacephei.com/vosk/models> y descomprímelo en una carpeta llamada
`model` o indica la ruta al crear `VoiceControl`.

Para probarlo ejecuta:

```bash
python voice_control.py --model path/a/tu/modelo --samplerate 16000
```

Habla después de que el programa indique que está escuchando y se mostrará el
texto reconocido.
