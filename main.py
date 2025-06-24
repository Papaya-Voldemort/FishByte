import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

import random
import os
import json
import helpers
import time
import tutorial
# FishByte Game





with open("save.json", "r") as file:
    volume = json.load(file).get("settings", {}).get("music_volume")
background_music_file = "song.wav"
helpers.play_background_music(background_music_file, volume)

save_file = "save.json"

with open("fish/new_fish.json", "r") as file:
    fish_data = json.load(file)

# Check if the save file exists if not create it
if not os.path.exists(save_file):
    with open(save_file, "w") as f:
        json.dump({"tickets": {}}, f, indent=4)
    with open("save_json.json", "w") as f:
        json.dump({"tickets": {}}, f, indent=4)
    print(helpers.color_text("Created save file...", "green"))
    print(helpers.color_text("Welcome to FishByte!", "cyan"))
else:
    print(helpers.color_text("Save file found...", "green"))
    print(helpers.color_text("Loading save file...", "green"))
    print(helpers.color_text("Welcome back to FishByte!", "cyan"))

with open(save_file, "r") as file:
    tutorial_completed = json.load(file).get("settings", {}).get("tutorial_completed", False)
if not tutorial_completed:
    question_the_player = True
    while question_the_player:
        print(helpers.color_text("It seems you haven't completed the tutorial yet.", "yellow"))
        wants_tutorial = input(helpers.color_text("Let's play the tutorial to get you started! (Y/N) ", "green"))
        if wants_tutorial.lower() == "y":
            print(helpers.color_text("Starting tutorial...", "cyan"))
            tutorial.play_tutorial()
            with open(save_file, "r") as file:
                data = json.load(file)
            if "settings" not in data:
                data["settings"] = {}
            data["settings"]["tutorial_completed"] = True
            with open(save_file, "w") as file:
                json.dump(data, file, indent=4)
            tutorial_completed = True
            question_the_player = False
        elif wants_tutorial.lower() == "n":
            confirm_skip = input(helpers.color_text("Are you SURE you want to skip the tutorial? (Y/N) ", "red"))
            if confirm_skip.lower() == "y":
                print(helpers.color_text("Fine... you can play it later by typing 'tutorial'.", "cyan"))
                question_the_player = False
            elif confirm_skip.lower() == 'n':
                continue
            else:
                print(helpers.color_text("Invalid input. Please type 'Y' or 'N'.", "red"))
        else:
            print(helpers.color_text("Invalid input. Please type 'Y' or 'N'.", "red"))

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
        print(helpers.color_text("\nYou can also type the number corresponding to the action (e.g., \'1\' for Fish).", "yellow"))
    elif user_input == "fish" or user_input == "1":
        print(helpers.color_text("--- Fishing Locations ---", "bold"))
        print("1. Home Pond")
        print("2. River")
        print("3. Lake")
        print("4. Shallow Ocean")
        print("5. Deep Ocean")
        print("-------------------------")
        location_choice = input(helpers.color_text("Where would you like to fish? (or 'exit') ", "yellow"))

        if location_choice.lower() == 'exit':
            continue

        location_name = ""
        required_ticket = None
        fish_data_file = "fish/new_fish.json"

        if location_choice == "1":
            location_name = "Home Pond"
            fish_data_file = "fish/new_fish.json"
        elif location_choice == "2":
            location_name = "River"
            required_ticket = "river"
            fish_data_file = "fish/river.json"
        elif location_choice == "3":
            location_name = "Lake"
            required_ticket = "lake"
            fish_data_file = "fish/lake.json"
        elif location_choice == "4":
            location_name = "Shallow Ocean"
            required_ticket = "shallow_ocean"
            fish_data_file = "fish/shallow_ocean.json"
        elif location_choice == "5":
            location_name = "Deep Ocean"
            required_ticket = "deep_ocean"
            fish_data_file = "fish/deep_ocean.json"
        else:
            print(helpers.color_text("Invalid location.", "red"))
            continue

        # Check for ticket
        if required_ticket:
            with open(save_file, "r") as file:
                data = json.load(file)
            if not data.get("tickets", {}).get(required_ticket, False):
                print(helpers.color_text(f"You need a ticket to fish at {location_name}.", "red"))
                continue

        # Load fish data
        current_fish_data = None
        try:
            with open(fish_data_file, "r") as file:
                current_fish_data = json.load(file)
                if not current_fish_data.get("fish"):
                    print(helpers.color_text(f"No fish defined for {location_name}. Using default fish.", "yellow"))
                    with open("fish/new_fish.json", "r") as f:
                        current_fish_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print(helpers.color_text(f"Could not load fish data for {location_name}. Using default fish.", "yellow"))
            with open("fish/new_fish.json", "r") as f:
                current_fish_data = json.load(f)

        is_fishing = False
        #global space_pressed, last_space_time, bar_color
        while True:
            if is_fishing:
                # When fishing is in progress, use a non-blocking input with timeout
                # This allows the progress bar to run without interruption
                time.sleep(0.1)  # Small delay to prevent CPU overuse
                continue

            action = input(helpers.color_text(f"Press enter to fish in {location_name}, or type 'exit' to return to the main menu: ", "cyan")).strip().lower()

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
                chosen_fish = helpers.fish(current_fish_data, fishing_rod)
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
                print(helpers.color_text("--- Your Fish Inventory ---", "bold"))
                for i, fish in enumerate(fish_inventory, start=1):
                    print(f"{i}. {fish}")
                print(helpers.color_text("---------------------------", "bold"))
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
                                fish_rarity = fish_item[fish_item.index("(") + 1:fish_item.index(")")]

                                # Find fish value from fish_data by checking all location files in the fish directory
                                fish_value = None
                                for loc_file in ["fish/new_fish.json", "fish/river.json", "fish/lake.json", "fish/shallow_ocean.json", "fish/deep_ocean.json"]:
                                    try:
                                        with open(loc_file, "r") as f:
                                            loc_fish_data = json.load(f)
                                            for fish in loc_fish_data.get("fish", []):
                                                if fish["name"] == fish_name:
                                                    rarity_info = fish["rarities"].get(fish_rarity)
                                                    if rarity_info:
                                                        fish_value = rarity_info["value"]
                                                        break
                                            if fish_value is not None:
                                                break
                                    except (FileNotFoundError, json.JSONDecodeError):
                                        continue
                                if fish_value is not None:
                                    total_value += fish_value
                                    sold_fish_count += 1


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
                            fish_rarity = sold_fish[sold_fish.index("(") + 1:sold_fish.index(")")]
                        else:
                            print(helpers.color_text("Invalid fish format, cannot sell.", "red"))
                            continue


                        # Find fish value from fish_data
                        fish_value = None
                        # Find fish value from fish_data by checking all location files
                        for loc_file in ["fish/new_fish.json", "fish/river.json", "fish/lake.json", "fish/shallow_ocean.json", "fish/deep_ocean.json"]:
                            try:
                                with open(loc_file, "r") as f:
                                    loc_fish_data = json.load(f)
                                    for fish in loc_fish_data.get("fish", []):
                                        if fish["name"] == fish_name:
                                            rarity_info = fish["rarities"].get(fish_rarity)
                                            if rarity_info:
                                                fish_value = rarity_info["value"]
                                                break
                                    if fish_value is not None:
                                        break
                            except (FileNotFoundError, json.JSONDecodeError):
                                continue

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
                print(helpers.color_text("No fish in inventory to sell.", "yellow"))
    elif user_input == "inventory" or user_input == "3":
        with open(save_file, "r") as file:
            data = json.load(file)
        if "inventory" in data and "fish" in data["inventory"]:
            fish_inventory = data["inventory"]["fish"]
            if fish_inventory:
                print(helpers.color_text("--- Your Fish Inventory ---", "bold"))
                for i, fish in enumerate(fish_inventory, start=1):
                    print(f"{i}. {fish}")
                print(helpers.color_text("---------------------------", "bold"))
            else:
                print(helpers.color_text("Your fish inventory is empty.", "yellow"))
        else:
            print(helpers.color_text("No fish in inventory.", "yellow"))
    elif user_input == "shop" or user_input == "4":
        with open(save_file, "r") as file:
            data = json.load(file)
        coins = data.get("coins", 0)
        print(helpers.color_text("--- Shop ---", "bold"))
        print(f"Your coins: {coins}")
        print("1. Buy new fishing rod")
        print("2. Buy Tickets")
        print("3. Exit")
        print(helpers.color_text("------------", "bold"))
        shop_choice = input(helpers.color_text("What would you like to do? ", "yellow"))
        if shop_choice == "1":
            print(helpers.color_text("--- Fishing Rods ---", "bold"))
            print("1. Basic Rod (10000 coins)")
            print("2. Advanced Rod (50000 coins)")
            print("3. Elite Rod (100000 coins)")
            print(helpers.color_text("--------------------", "bold"))
            rod_choice = input(helpers.color_text("Which rod would you like to buy? ", "yellow"))
            if rod_choice == "1":
                print(helpers.color_text("You already have the Basic Rod.", "yellow"))
            elif rod_choice == "2":
                if coins >= 50000:
                    helpers.edit_json(save_file, "coins", coins - 50000)
                    helpers.edit_json(save_file, "fishing_rod", "Advanced")
                    print(helpers.color_text("You bought the Advanced Rod!", "green"))
                else:
                    print(helpers.color_text("You don't have enough coins to buy the Advanced Rod.", "red"))
            elif rod_choice == "3":
                if coins >= 100000:
                    helpers.edit_json(save_file, "coins", coins - 100000)
                    helpers.edit_json(save_file, "fishing_rod", "Elite")
                    print(helpers.color_text("You bought the Elite Rod!", "green"))
                else:
                    print(helpers.color_text("You don't have enough coins to buy the Elite Rod.", "red"))
            else:
                print(helpers.color_text("Invalid choice.", "red"))
        elif shop_choice == "2":
            with open(save_file, "r") as file:
                data = json.load(file)
            tickets = data.get("tickets", {})
            coins = data.get("coins", 0)
            ticket_prices = {
                "river": 1000,
                "lake": 2500,
                "shallow_ocean": 5000,
                "deep_ocean": 10000
            }

            print(helpers.color_text("--- Buy Tickets ---", "bold"))

            ticket_options = []
            if not tickets.get("river"):
                ticket_options.append(("river", "River Ticket", ticket_prices["river"]))
            if not tickets.get("lake"):
                ticket_options.append(("lake", "Lake Ticket", ticket_prices["lake"]))
            if not tickets.get("shallow_ocean"):
                ticket_options.append(("shallow_ocean", "Shallow Ocean Ticket", ticket_prices["shallow_ocean"]))
            if not tickets.get("deep_ocean"):
                ticket_options.append(("deep_ocean", "Deep Ocean Ticket", ticket_prices["deep_ocean"]))

            if not ticket_options:
                print(helpers.color_text("You have purchased all available tickets!", "green"))
                continue

            for i, (key, name, price) in enumerate(ticket_options, 1):
                print(f"{i}. {name} ({price} coins)")

            print(helpers.color_text("-------------------", "bold"))
            ticket_choice = input(helpers.color_text("Which ticket would you like to buy? (or 'exit') ", "yellow"))

            if ticket_choice.lower() == 'exit':
                continue

            try:
                choice_num = int(ticket_choice)
                if 1 <= choice_num <= len(ticket_options):
                    chosen_ticket_key, chosen_ticket_name, chosen_ticket_price = ticket_options[choice_num - 1]

                    if coins >= chosen_ticket_price:
                        data["coins"] = coins - chosen_ticket_price
                        if "tickets" not in data:
                            data["tickets"] = {}
                        data["tickets"][chosen_ticket_key] = True

                        with open(save_file, "w") as file:
                            json.dump(data, file, indent=4)
                        with open("save_json.json", "w") as file:
                            json.dump(data, file, indent=4)

                        print(helpers.color_text(f"You bought the {chosen_ticket_name}!", "green"))
                    else:
                        print(helpers.color_text("You don't have enough coins.", "red"))
                else:
                    print(helpers.color_text("Invalid choice.", "red"))
            except ValueError:
                print(helpers.color_text("Invalid input.", "red"))
        elif shop_choice == "3":
            pass
        else:
            print(helpers.color_text("Invalid choice.", "red"))
    elif user_input == "save" or user_input == "5":
        with open(save_file, "w") as file:
            json.dump(data, file, indent=4)
        with open("save_json.json", "w") as file:
            json.dump(data, file, indent=4)
        print(helpers.color_text("Game saved!", "green"))
    elif user_input == "exit" or user_input == "6":
        with open(save_file, "w") as file:
            json.dump(data, file, indent=4)
        with open("save_json.json", "w") as file:
            json.dump(data, file, indent=4)
        print(helpers.color_text("Game saved. Goodbye!", "green"))
        break
    elif user_input == "tutorial" or user_input == "7":
        tutorial.play_tutorial()
    elif user_input == "reset" or user_input == "8":
        confirm = input(helpers.color_text("Are you sure you want to reset your game? This cannot be undone. (Y/N) ", "red"))
        if confirm.lower() == "y":
            with open(save_file, "w") as f:
                f.write("{}")
            print(helpers.color_text("Game reset.", "green"))
        else:
            print(helpers.color_text("Reset cancelled.", "yellow"))
    elif user_input == "gallery" or user_input == "9":
        with open(save_file, "r") as file:
            data = json.load(file)
        if "gallery" in data:
            print(helpers.color_text("--- Fish Gallery ---", "bold"))
            for fish_name, rarities in data["gallery"].items():
                rarity_list = ", ".join(rarities.keys())
                print(f"{fish_name}: Caught - {rarity_list}")
            print(helpers.color_text("--------------------", "bold"))
        else:
            print(helpers.color_text("Your gallery is empty. Go catch some fish!", "yellow"))
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
