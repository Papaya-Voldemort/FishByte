import random
import json
import simpleaudio as sa
import threading
from pydub import AudioSegment
import sys
import colorama
from colorama import Fore, Style
import time

# Platform-specific imports for input handling
if sys.platform == "win32":
    import msvcrt
else:
    import termios
    import select

colorama.init(autoreset=True)

def color_text(text, color):
    colors = {
        "red": Fore.RED,
        "green": Fore.GREEN,
        "yellow": Fore.YELLOW,
        "blue": Fore.BLUE,
        "magenta": Fore.MAGENTA,
        "cyan": Fore.CYAN,
        "white": Fore.WHITE,
        "purple": Fore.MAGENTA,
        "orange": Fore.YELLOW,
        "bold": Style.BRIGHT,
        "reset": Style.RESET_ALL
    }
    return f"{colors.get(color, Style.RESET_ALL)}{text}{Style.RESET_ALL}"


def fish(fish_data, fishing_rod):
    weighted_choices = []
    weights = []

    # Collect all fish rarities with their catch rates for the given fishing level
    for fish in fish_data["fish"]:
        for rarity, stats in fish["rarities"].items():
            catch_rate = stats["catch_rate"].get(fishing_rod, 0)
            if catch_rate > 0:
                weighted_choices.append((fish["name"], rarity, stats))
                weights.append(catch_rate)

    # Use random.choices to pick one based on weights
    chosen = random.choices(weighted_choices, weights=weights, k=1)[0]
    return chosen

def edit_json(file_path, key, value):
    """
    Adds or edits data in a JSON file.

    Args:
        file_path (str): The path to the JSON file.
        key (str): The key to add or edit (can be nested, e.g., "inventory.fish").
        value: The value to associate with the key.
    """
    data = {}
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        pass # data is already {} so we will create a new file

    keys = key.split('.')
    current = data

    for i, k in enumerate(keys[:-1]):
        if k not in current:
            current[k] = {}
        current = current[k]

    # If the key is 'inventory.fish', append the value to the list
    if keys[-1] == 'fish' and keys[-2] == 'inventory':
        if not isinstance(value, list):
            # Append a single fish string
            if keys[-1] not in current or not isinstance(current[keys[-1]], list):
                current[keys[-1]] = []
            current[keys[-1]].append(value)
        else:
            # Overwrite the whole fish list instead of appending
            current[keys[-1]] = value
    else:
        current[keys[-1]] = value

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)  # Write the updated data back to the file with indentation for readability


def play_background_music(filename, volume_change_db=0):
    """Plays background music in a loop, supports .mp3 and .wav natively."""
    try:
        if filename.lower().endswith(".mp3"):
            # Load mp3 and convert to WaveObject directly
            sound = AudioSegment.from_mp3(filename)
            # Adjust volume
            sound += volume_change_db
            # Convert to raw data
            raw_data = sound.raw_data
            # Get frame rate, sample width, and channels
            frame_rate = sound.frame_rate
            sample_width = sound.sample_width
            channels = sound.channels
            # Load raw data into WaveObject
            wave_obj = sa.WaveObject(
                raw_data,
                num_channels=channels,
                bytes_per_sample=sample_width,
                sample_rate=frame_rate
            )
        elif filename.lower().endswith(".wav"):
            # Load wav file
            sound = AudioSegment.from_wav(filename)
            # Adjust volume
            sound += volume_change_db
            # Convert to raw data
            raw_data = sound.raw_data
            # Get frame rate, sample width, and channels
            frame_rate = sound.frame_rate
            sample_width = sound.sample_width
            channels = sound.channels
            # Load raw data into WaveObject
            wave_obj = sa.WaveObject(
                raw_data,
                num_channels=channels,
                bytes_per_sample=sample_width,
                sample_rate=frame_rate
            )
        else:
            print(f"Error: Unsupported file format. Only .mp3 and .wav are supported.")
            return
    except FileNotFoundError:
        print(f"Error: '{filename}' not found. Music will not play.")
        return
    except Exception as e:
        print(f"Error loading '{filename}': {e}")
        return

    def loop_music():
        play_obj = None
        while True:
            try:
                if play_obj is None or not play_obj.is_playing():
                    play_obj = wave_obj.play()
                time.sleep(0.1)
            except Exception as e:
                print(f"Error playing music: {e}")
                break

    # Create and start the music thread
    music_thread = threading.Thread(target=loop_music, daemon=True)
    music_thread.start()


def flush_input():
    """Flushes the input buffer."""
    if sys.platform == "win32":
        while msvcrt.kbhit():
            msvcrt.getch()
    else:
        try:
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)
        except (AttributeError, termios.error):
            pass

def is_input_waiting():
    """Checks if there is input waiting on stdin."""
    if sys.platform == "win32":
        return msvcrt.kbhit()
    else:
        try:
            # On Windows, this will not work. But the user is on macOS.
            # The `select` call checks for readability on stdin with a timeout of 0.
            return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])
        except:
            return False
