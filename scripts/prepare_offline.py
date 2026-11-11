"""Pre-download runtime assets once so the local app can work without Wi-Fi.

Check:    python -m scripts.prepare_offline
Download: python -m scripts.prepare_offline --download
Needs temporary internet only with --download. Does not access patient records.
"""
import argparse
import subprocess
import sys
from config.settings import OLLAMA_MODEL, WHISPER_MODEL
from services.offline_status import inspect_offline


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--download',action='store_true')
    args=p.parse_args()
    if args.download:
        print('Downloading Ollama model (public model files only)...')
        try:
            subprocess.run(['ollama','pull',OLLAMA_MODEL],check=True)
        except (FileNotFoundError,subprocess.CalledProcessError):
            print('Ollama download failed: install/start Ollama and retry.',file=sys.stderr)
            raise SystemExit(2)
        print('Downloading public Whisper speech model...')
        from faster_whisper import WhisperModel
        WhisperModel(WHISPER_MODEL,device='cpu',compute_type='int8')
    status=inspect_offline()
    for key,val in status.items():
        print(f'{key}: {val}')
    print('Optional image OCR additionally requires Tesseract and pip install -r requirements-ocr.txt.')
    print('Offline translation depends on prepared local locale packs; browser speech output depends on installed voices.')

if __name__=='__main__': main()
