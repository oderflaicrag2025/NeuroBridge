import json
import queue
import os
import sys
import argparse
from typing import Optional, List, Any
try:
    import sounddevice as sd
except OSError as exc:  # PortAudio missing
    sd = None
    SD_IMPORT_ERROR = exc
else:
    SD_IMPORT_ERROR = None
import vosk


class VoiceControl:
    """Offline voice control module using Vosk."""

    def __init__(self, model_path: str = "model", samplerate: int = 16000):
        if SD_IMPORT_ERROR is not None:
            print(
                "sounddevice library could not be loaded: install PortAudio to "
                "enable microphone input",
                file=sys.stderr,
            )
            self.disabled = True
        else:
            self.disabled = False

        if not os.path.isdir(model_path):
            raise FileNotFoundError(
                f"Vosk model not found at '{model_path}'. "
                "Download a model from https://alphacephei.com/vosk/models and "
                "provide its path via the 'model_path' argument."
            )
        self.model = vosk.Model(model_path)
        self.samplerate = samplerate
        self.recognizer = vosk.KaldiRecognizer(self.model, self.samplerate)
        self._queue: queue.Queue[bytes] = queue.Queue()

    def _callback(
        self,
        indata: bytes,
        frames: int,
        time_info: Any,
        status: Any,
    ) -> None:
        if status:
            print(status, file=sys.stderr)
        self._queue.put(bytes(indata))

    def listen(self) -> str:
        """Listen for a single phrase and return the recognized text."""
        if self.disabled:
            raise RuntimeError(
                "Microphone input is not available; install PortAudio and the"
                " sounddevice package."
            )
        with sd.RawInputStream(
            samplerate=self.samplerate,
            blocksize=8000,
            dtype="int16",
            channels=1,
            callback=self._callback,
        ):
            print("Listening...")
            while True:
                data = self._queue.get()
                if self.recognizer.AcceptWaveform(data):
                    result = self.recognizer.Result()
                    text = json.loads(result).get("text", "")
                    print(f"You said: {text}")
                    return text


def main(argv: Optional[List[str]] = None) -> None:
    """Run the voice control demo from the command line."""
    parser = argparse.ArgumentParser(description="Offline speech recognition")
    parser.add_argument(
        "--model",
        default="model",
        help="Ruta al modelo de Vosk (carpeta descomprimida)",
    )
    parser.add_argument(
        "--samplerate",
        type=int,
        default=16000,
        help="Frecuencia de muestreo del micr\xf3fono",
    )
    args = parser.parse_args(argv)
    vc = VoiceControl(model_path=args.model, samplerate=args.samplerate)
    vc.listen()


if __name__ == "__main__":
    main()
