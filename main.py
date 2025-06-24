import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

import random
import os
import json
import helpers
import time
import tutorial
# FishByte Game






# TODO Make sound volume adjustable from the save settings
with open("save.json", "r") as file:
    volume = json.load(file).get("settings", {}).get("music_volume")
background_music_file = "song.wav"
helpers.play_background_music(background_music_file, volume)

save_file = "save.json"

with open("new_fish.json", "r") as file:
    fish_data = json.load(file)

# Check if the save file exists
if not os.path.exists(save_file):
    with open(save_file, "w") as f:
        f.write("{}")
    print(helpers.color_text("Created save file...", "green"))
    print(helpers.color_text("Welcome to FishByte!", "cyan"))
else:
    print(helpers.color_text("Save file found...", "green"))
    print(helpers.color_text("Loading save file...", "green"))
    print(helpers.color_text("Welcome back to FishByte!", "cyan"))

# Load the save data
with open(save_file, "r") as file:
    data = json.load(file)

# Check if 'fishing_rod' exists in the save data, otherwise default to "Basic"
fishing_rod = data.get("fishing_rod", "Basic")

last_fish_time = 0

while True:
    user_input = input(helpers.color_text("What would you like to do? (type 'help' for options): ", "yellow")).strip().lower()
    if user_input == "help":
        print(helpers.color_text("Options: ", "bold"))
        print(helpers.color_text("1. Fish", "cyan"))
        print(helpers.color_text("2. Sell Fish", "cyan"))
        print(helpers.color_text("3. View Inventory", "cyan"))
        print(helpers.color_text("4. Enter Shop", "cyan"))
        print(helpers.color_text("5. Save Game", "cyan"))
        print(helpers.color_text("6. Exit", "cyan"))
        print(helpers.color_text("7. Play Tutorial", "cyan"))
        print(helpers.color_text("8. Reset Game", "cyan"))
        print(helpers.color_text("9. Gallery", "cyan"))
        print(helpers.color_text("10. Stats", "cyan"))
        print(helpers.color_text("\nYou can also type the number corresponding to the action (e.g., '1' for Fish).", "yellow"))
    elif user_input == "fish" or user_input == "1":
        is_fishing = False
        #global space_pressed, last_space_time, bar_color
        while True:
            if is_fishing:
                # When fishing is in progress, use a non-blocking input with timeout
                # This allows the progress bar to run without interruption
                time.sleep(0.1)  # Small delay to prevent CPU overuse
                continue

            action = input(helpers.color_text("Press enter to fish, or type 'exit' to return to the main menu: ", "cyan")).strip().lower()

            if action == "exit":
                print(helpers.color_text("You stopped fishing.", "yellow"))
                break  # Exit the fishing loop

            if action == "":
                is_fishing = True
                current_time = time.time()
                if current_time - last_fish_time < 1:
                    #print("Please wait a moment before fishing again...")
                    is_fishing = False
                    continue

                # Determine the fish before showing the loading bar
                chosen_fish = helpers.fish(fish_data, fishing_rod)
                fish_rarity = chosen_fish[1]

                # --- NEW FISHING MINI-GAME ---
                print(helpers.color_text("Pulling in the fish...", "yellow"))
                time.sleep(random.uniform(0.5, 2.0))  # Wait for a random time before showing the prompt

                # Check for premature input (spamming)
                if helpers.is_input_waiting():
                    print(helpers.color_text("You scared the fish away by making too much noise!", "red"))
                    helpers.flush_input() # Clear the spam
                    is_fishing = False
                    last_fish_time = time.time()
                    continue

                helpers.flush_input()  # Clear the input buffer
                print(helpers.color_text("!!! PRESS ENTER NOW !!!", "red"))
                start_time = time.time()
                input()
                end_time = time.time()

                reaction_time = end_time - start_time

                # Difficulty scales with rarity of the fish
                max_reaction_time = {
                    "Bronze": 2.0,
                    "Silver": 1.5,
                    "Gold": 1.0,
                    "Platinum": 0.8,
                    "Diamond": 0.7,
                    "Mythic": 0.6,
                    "Void": 0.5,
                    "Celestial": 0.4,
                    "Ancient Fossil": 0.3
                }.get(fish_rarity, 2.0)

                if reaction_time > max_reaction_time:
                    print(helpers.color_text(f"Too slow! Your reaction time of {reaction_time:.2f}s wasn't fast enough. The fish got away.", "red"))
                    is_fishing = False
                    last_fish_time = time.time()
                    continue

                print(helpers.color_text(f"Nice! You reacted in {reaction_time:.2f}s.", "green"))
                # --- END OF MINI-GAME ---

                print(helpers.color_text("Fish caught!", "green"))
                print(f"Chosen fish: {helpers.color_text(chosen_fish[0], 'blue')}, Rarity: {helpers.color_text(chosen_fish[1], 'purple')}, Stats: {chosen_fish[2]}")
                helpers.edit_json(save_file, "inventory.fish", chosen_fish[0] + " (" + chosen_fish[1] + ")")
                import json

                # Update gallery in save file after catching a fish
                fish_name = chosen_fish[0]
                fish_rarity = chosen_fish[1]

                with open(save_file, "r") as file:
                    data = json.load(file)

                if "gallery" not in data:
                    data["gallery"] = {}

                if fish_name not in data["gallery"]:
                    data["gallery"][fish_name] = {}

                data["gallery"][fish_name][fish_rarity] = True

                with open(save_file, "w") as file:
                    json.dump(data, file, indent=4)
                with open(save_file, "r") as file:
                    data = json.load(file)
                current_xp = data.get("xp", 0)
                helpers.edit_json(save_file, "xp", current_xp + 10)
                last_fish_time = time.time()
                is_fishing = False  # Reset fishing status after completion
                continue
            else:
                print(helpers.color_text("Invalid input. Please press Enter to fish or type 'exit' to stop.", "red"))
        continue  # Return to the main game loop after fishing
    elif user_input == "sell fish" or user_input == "2" or user_input == "sell":
        with open(save_file, "r") as file:
            data = json.load(file)
        if "inventory" in data and "fish" in data["inventory"]:
            fish_inventory = data["inventory"]["fish"]
            if fish_inventory:
                print(helpers.color_text("Your fish inventory:", "bold"))
                for i, fish in enumerate(fish_inventory, start=1):
                    print(f"{i}. {fish}")
                try:
                    choice = input(helpers.color_text("Enter the number of the fish you want to sell (or 'all' to sell everything): ", "yellow"))
                    if choice == "all":
                        # Sell all fish functionality
                        total_value = 0
                        sold_fish_count = 0

                        # Calculate total value of all fish
                        for fish_item in fish_inventory:
                            # Parse fish name and rarity
                            if "(" in fish_item and ")" in fish_item:
                                fish_name = fish_item[:fish_item.index("(")].strip()
                                fish_rarity = fish_item[fish_item.index("(")+1:fish_item.index(")")]

                                # Find fish value from fish_data
                                for fish in fish_data["fish"]:
                                    if fish["name"] == fish_name:
                                        rarity_info = fish["rarities"].get(fish_rarity)
                                        if rarity_info:
                                            total_value += rarity_info["value"]
                                            sold_fish_count += 1
                                            break

                        # Update coins
                        coins = data.get("coins", 0)
                        coins += total_value

                        # Save updated coins to file
                        helpers.edit_json(save_file, "coins", coins)

                        # Clear fish inventory
                        helpers.edit_json(save_file, "inventory.fish", [])

                        print(helpers.color_text(f"You sold {sold_fish_count} fish for a total of {total_value} coins!", "green"))
                        continue

                    choice_num = int(choice)
                    if 1 <= choice_num <= len(fish_inventory):
                        sold_fish = fish_inventory.pop(choice_num - 1)
                        # Parse fish name and rarity
                        if "(" in sold_fish and ")" in sold_fish:
                            fish_name = sold_fish[:sold_fish.index("(")].strip()
                            fish_rarity = sold_fish[sold_fish.index("(")+1:sold_fish.index(")")]
                        else:
                            print(helpers.color_text("Invalid fish format, cannot sell.", "red"))
                            continue


                        # Find fish value from fish_data
                        fish_value = None
                        for fish in fish_data["fish"]:
                            if fish["name"] == fish_name:
                                rarity_info = fish["rarities"].get(fish_rarity)
                                if rarity_info:
                                    fish_value = rarity_info["value"]
                                    break

                        if fish_value is None:
                            print(helpers.color_text("Could not find the value of this fish. Sell cancelled.", "red"))
                            continue

                        # Update fish inventory in save file
                        helpers.edit_json(save_file, "inventory.fish", fish_inventory)

                        # Add coins for the sold fish
                        coins = data.get("coins", 0)
                        coins += fish_value

                        # Save updated coins to save file
                        helpers.edit_json(save_file, "coins", coins)

                        print(helpers.color_text(f"You sold {sold_fish} for {fish_value} coins!", "green"))
                    else:
                        print(helpers.color_text("Invalid choice.", "red"))
                except ValueError:
                    print(helpers.color_text("Please enter a valid number.", "red"))
            else:
                print(helpers.color_text("Your fish inventory is empty.", "yellow"))
        else:
            print(helpers.color_text("No fish found in inventory.", "yellow"))
    elif user_input == "view inventory" or user_input == "3" or user_input == "inventory":
        with open(save_file, "r") as file:
            data = json.load(file)

        # Display coins
        coins = data.get("coins", 0)
        print(f"{helpers.color_text('Coins:', 'bold')} {helpers.color_text(str(coins), 'yellow')}")

        # Display fishing rod
        fishing_rod = data.get("fishing_rod", "Basic")
        print(f"{helpers.color_text('Fishing Rod:', 'bold')} {fishing_rod}")

        # Display XP if it exists
        if "xp" in data:
            print(f"{helpers.color_text('XP:', 'bold')} {data['xp']}")

        # Display fish inventory
        if "inventory" in data and "fish" in data["inventory"]:
            fish_inventory = data["inventory"]["fish"]
            if fish_inventory:
                print(helpers.color_text("\nYour fish inventory:", "bold"))
                for i, fish in enumerate(fish_inventory, start=1):
                    print(f"{i}. {fish}")
            else:
                print(helpers.color_text("\nYour fish inventory is empty, catch some fish!", "yellow"))
        else:
            print(helpers.color_text("\nNo fish found in inventory.", "yellow"))

        # Display other items if they exist
        if "inventory" in data:
            for item_type, items in data["inventory"].items():
                if item_type != "fish" and items:  # Skip fish as we already displayed them
                    print(f"\n{helpers.color_text(f'Your {item_type} inventory:', 'bold')}")
                    if isinstance(items, list):
                        for i, item in enumerate(items, start=1):
                            print(f"{i}. {item}")
                    else:
                        print(items)  # If it's not a list, just print the values of the fish inventory
    elif user_input == "enter shop" or user_input == "4" or user_input == "shop":
        print(helpers.color_text("Welcome to the FishByte Shop!", "bold"))
        print(helpers.color_text("Available items for purchase:", "cyan"))

        # Define shop items with their names, costs, and rod types
        shop_items = {
            "1": {"name": "Basic Fishing Rod", "cost": 10000, "rod": "Basic"},
            "2": {"name": "Advanced Fishing Rod", "cost": 50000, "rod": "Advanced"},
            "3": {"name": "Elite Fishing Rod", "cost": 100000, "rod": "Elite"},
            "4": {"name": "Exit Shop"}
        }

        # Display shop items
        for key, item in shop_items.items():
            if key != "4":
                print(f"{key}. {helpers.color_text(item['name'], 'blue')} - {helpers.color_text(str(item['cost']), 'yellow')} coins")
            else:
                print(f"{key}. {item['name']}")

        query = input(helpers.color_text("Enter the number of the item you want to purchase: ", "yellow"))

        if query in shop_items:
            selected_item = shop_items[query]

            if query == "4":
                print(helpers.color_text("Exiting shop...", "yellow"))
            else:
                item_name = selected_item['name']
                item_cost = selected_item['cost']
                item_rod = selected_item['rod']

                # Check if the player has enough coins
                if data.get("coins", 0) >= item_cost:
                    # Deduct coins and update fishing rod
                    helpers.edit_json(save_file, "coins", data.get("coins", 0) - item_cost)
                    helpers.edit_json(save_file, "fishing_rod", item_rod)
                    fishing_rod = item_rod  # Update the local variable
                    print(helpers.color_text(f"You have purchased the {item_name}!", "green"))
                else:
                    print(helpers.color_text("You do not have enough coins to purchase this item.", "red"))
        else:
            print(helpers.color_text("Invalid option. Please try again.", "red"))

    elif user_input == "save game" or user_input == "5" or user_input == "save":
        print(helpers.color_text("Saving game...", "green"))
        with open(save_file, "w") as file:
            json.dump(data, file, indent=4)
    elif user_input == "exit" or user_input == "6" or user_input == "quit" or user_input == "exit game":
        print(helpers.color_text("Exiting game. Goodbye!", "yellow"))
        break
        exit()
    elif user_input == "play tutorial" or user_input == "7" or user_input == "tutorial":
        print(helpers.color_text("Playing tutorial...", "cyan"))
        tutorial.play_tutorial()
    elif user_input == "reset game" or user_input == "8" or user_input == "reset":
        print(helpers.color_text("Resetting game...", "red"))
        if os.path.exists(save_file):
            os.remove(save_file)
        default_data = {
            "coins": 0,
            "fishing_rod": "Basic",
            "xp": 0,
            "inventory": {
                "fish": []
            },
            "stats": {
                "total_fish_caught": 0,
                "most_valuable_fish": {
                    "name": None,
                    "value": 0
                }
            },
            "settings": {
                "music_volume": 1.0,
                "effects_volume": 1.0
            },
            "gallery": {}
        }
        with open(save_file, "w") as f:
            json.dump(default_data, f, indent=4)
        data = default_data
        print(helpers.color_text("Game reset. Welcome to FishByte!", "green"))
        data = default_data
    elif user_input == "gallery" or user_input == "9":
        print(helpers.color_text("Welcome to the FishByte Gallery!", "bold"))
        with open(save_file, "r") as file:
            data = json.load(file)

        if "gallery" in data and data["gallery"]:
            print(helpers.color_text("{:<20} {:<15}".format("Fish Name", "Rarity"), "bold"))
            print("-" * 35)
            for fish_name, rarities in data["gallery"].items():
                rarity_list = [r for r, c in rarities.items() if c]
                if rarity_list:
                    print("{:<20} {:<15}".format(fish_name, ", ".join(rarity_list)))
        else:
            print(helpers.color_text("Your gallery is empty. Catch some fish to fill it up!", "yellow"))
    elif user_input == "stats" or user_input == "10":
        with open(save_file, "r") as file:
            data = json.load(file)
        if "stats" in data:
            print(helpers.color_text("--- Your Stats ---", "bold"))
            print(f"Total fish caught: {data['stats'].get('total_fish_caught', 0)}")
            most_valuable = data['stats'].get('most_valuable_fish', {})
            if most_valuable.get('name'):
                print(f"Most valuable fish: {most_valuable.get('name')} ({most_valuable.get('value', 0)} coins)")
            else:
                print("Most valuable fish: None")
            print("------------------")
        else:
            print("No stats found. Catch some fish to see your stats!")
    else:
        print("Invalid command. Type 'help' for options.")
