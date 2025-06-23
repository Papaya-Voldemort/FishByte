from setuptools import setup

APP = ['main.py']
DATA_FILES = ['fish.json', 'new_fish.json', 'save_json.json', 'save.json', 'song.wav']
OPTIONS = {
    'argv_emulation': True,
    'packages': ['tqdm', 'simpleaudio', 'pydub'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
