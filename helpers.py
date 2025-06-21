import random
import json

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
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}  # Create an empty dictionary if the file doesn't exist

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
            if not isinstance(current[keys[-1]], list):
                current[keys[-1]] = []
            current[keys[-1]].append(value)
        else:
            # Overwrite the whole fish list instead of appending
            current[keys[-1]] = value
    else:
        current[keys[-1]] = value

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)  # Write the updated data back to the file with indentation for readability