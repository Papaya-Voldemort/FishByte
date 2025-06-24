import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

import random
import os
import json
import helpers
import time
import tqdm
import tutorial





# TODO Make sound volume adjustable from the save settings
background_music_file = "song.wav"
helpers.play_background_music(background_music_file)

save_file = "save.json"

with open("new_fish.json", "r") as file:
    fish_data = json.load(file)

# Check if the save file exists
if not os.path.exists(save_file):
    with open(save_file, "w") as f:
        f.write("{}")
    print("Created save file...")
    print("Welcome to FishByte!")
else:
    print("Save file found...")
    print("Loading save file...")
    print("Welcome back to FishByte!")

# Load the save data
with open(save_file, "r") as file:
    data = json.load(file)

# Check if 'fishing_rod' exists in the save data, otherwise default to "Basic"
fishing_rod = data.get("fishing_rod", "Basic")

last_fish_time = 0

while True:
    user_input = input("What would you like to do? (type 'help' for options): ").strip().lower()
    if user_input == "help":
        print("Options: "
              "\n1. Fish "
              "\n2. Sell Fish "
              "\n3. View Inventory "
              "\n4. Enter Shop "
              "\n5. Save Game "
              "\n6. Exit "
              "\n7. Play Tutorial"
              "\n8. Reset Game"
              "\n9. Gallery"
              "\n10. Stats"
              "\n\nYou can also type the number corresponding to the action (e.g., '1' for Fish).")
    elif user_input == "fish" or user_input == "1":
        is_fishing = False
        #global space_pressed, last_space_time, bar_color
        while True:
            if is_fishing:
                # When fishing is in progress, use a non-blocking input with timeout
                # This allows the progress bar to run without interruption
                time.sleep(0.1)  # Small delay to prevent CPU overuse
                continue

            action = input("Press enter to fish, or type 'exit' to return to the main menu: ").strip().lower()

            if action == "exit":
                print("You stopped fishing.")
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
                print("Pulling in the fish...")
                time.sleep(random.uniform(0.5, 2.0))  # Wait for a random time before showing the prompt

                # Check for premature input (spamming)
                if helpers.is_input_waiting():
                    print("You scared the fish away by making too much noise!")
                    helpers.flush_input() # Clear the spam
                    is_fishing = False
                    last_fish_time = time.time()
                    continue

                helpers.flush_input()  # Clear the input buffer
                print("!!! PRESS ENTER NOW !!!")
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
                    print(f"Too slow! Your reaction time of {reaction_time:.2f}s wasn't fast enough. The fish got away.")
                    is_fishing = False
                    last_fish_time = time.time()
                    continue

                print(f"Nice! You reacted in {reaction_time:.2f}s.")
                # --- END OF MINI-GAME ---

                print("Fish caught!")
                print(f"Chosen fish: {chosen_fish[0]}, Rarity: {chosen_fish[1]}, Stats: {chosen_fish[2]}")
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
                print("Invalid input. Please press Enter to fish or type 'exit' to stop.")
        continue  # Return to the main game loop after fishing
    elif user_input == "sell fish" or user_input == "2" or user_input == "sell":
        with open(save_file, "r") as file:
            data = json.load(file)
        if "inventory" in data and "fish" in data["inventory"]:
            fish_inventory = data["inventory"]["fish"]
            if fish_inventory:
                print("Your fish inventory:")
                for i, fish in enumerate(fish_inventory, start=1):
                    print(f"{i}. {fish}")
                try:
                    choice = input("Enter the number of the fish you want to sell (or 'all' to sell everything): ")
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

                        print(f"You sold {sold_fish_count} fish for a total of {total_value} coins!")
                        continue

                    choice_num = int(choice)
                    if 1 <= choice_num <= len(fish_inventory):
                        sold_fish = fish_inventory.pop(choice_num - 1)
                        # Parse fish name and rarity
                        if "(" in sold_fish and ")" in sold_fish:
                            fish_name = sold_fish[:sold_fish.index("(")].strip()
                            fish_rarity = sold_fish[sold_fish.index("(")+1:sold_fish.index(")")]
                        else:
                            print("Invalid fish format, cannot sell.")
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
                            print("Could not find the value of this fish. Sell cancelled.")
                            continue

                        # Update fish inventory in save file
                        helpers.edit_json(save_file, "inventory.fish", fish_inventory)

                        # Add coins for the sold fish
                        coins = data.get("coins", 0)
                        coins += fish_value

                        # Save updated coins to save file
                        helpers.edit_json(save_file, "coins", coins)

                        print(f"You sold {sold_fish} for {fish_value} coins!")
                    else:
                        print("Invalid choice.")
                except ValueError:
                    print("Please enter a valid number.")
            else:
                print("Your fish inventory is empty.")
        else:
            print("No fish found in inventory.")
    elif user_input == "view inventory" or user_input == "3" or user_input == "inventory":
        with open(save_file, "r") as file:
            data = json.load(file)

        # Display coins
        coins = data.get("coins", 0)
        print(f"Coins: {coins}")

        # Display fishing rod
        fishing_rod = data.get("fishing_rod", "Basic")
        print(f"Fishing Rod: {fishing_rod}")

        # Display XP if it exists
        if "xp" in data:
            print(f"XP: {data['xp']}")

        # Display fish inventory
        if "inventory" in data and "fish" in data["inventory"]:
            fish_inventory = data["inventory"]["fish"]
            if fish_inventory:
                print("\nYour fish inventory:")
                for i, fish in enumerate(fish_inventory, start=1):
                    print(f"{i}. {fish}")
            else:
                print("\nYour fish inventory is empty, catch some fish!")
        else:
            print("\nNo fish found in inventory.")

        # Display other items if they exist
        if "inventory" in data:
            for item_type, items in data["inventory"].items():
                if item_type != "fish" and items:  # Skip fish as we already displayed them
                    print(f"\nYour {item_type} inventory:")
                    if isinstance(items, list):
                        for i, item in enumerate(items, start=1):
                            print(f"{i}. {item}")
                    else:
                        print(items)  # If it's not a list, just print the values of the fish inventory
    elif user_input == "enter shop" or user_input == "4" or user_input == "shop":
        print("Welcome to the FishByte Shop!")
        print("Available items for purchase:")

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
                print(f"{key}. {item['name']} - {item['cost']} coins")
            else:
                print(f"{key}. {item['name']}")

        query = input("Enter the number of the item you want to purchase: ")

        if query in shop_items:
            selected_item = shop_items[query]

            if query == "4":
                print("Exiting shop...")
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
                    print(f"You have purchased the {item_name}!")
                else:
                    print("You do not have enough coins to purchase this item.")
        else:
            print("Invalid option. Please try again.")

    elif user_input == "save game" or user_input == "5" or user_input == "save":
        print("Saving game...")
        with open(save_file, "w") as file:
            json.dump(data, file, indent=4)
    elif user_input == "exit" or user_input == "6" or user_input == "quit" or user_input == "exit game":
        print("Exiting game. Goodbye!")
        break
        exit()
    elif user_input == "play tutorial" or user_input == "7" or user_input == "tutorial":
        print("Playing tutorial...")
        tutorial.play_tutorial()
    elif user_input == "reset game" or user_input == "8" or user_input == "reset":
        print("Resetting game...")
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
        print("Game reset. Welcome to FishByte!")
        data = default_data
    elif user_input == "gallery" or user_input == "9":
        print("Welcome to the FishByte Gallery!")
        with open(save_file, "r") as file:
            data = json.load(file)

        if "gallery" in data and data["gallery"]:
            print("{:<20} {:<15}".format("Fish Name", "Rarity"))
            print("-" * 35)
            for fish_name, rarities in data["gallery"].items():
                rarity_list = [r for r, c in rarities.items() if c]
                if rarity_list:
                    print("{:<20} {:<15}".format(fish_name, ", ".join(rarity_list)))
        else:
            print("Your gallery is empty. Catch some fish to fill it up!")
    elif user_input == "stats" or user_input == "10":
        with open(save_file, "r") as file:
            data = json.load(file)
        if "stats" in data:
            print("--- Your Stats ---")
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
