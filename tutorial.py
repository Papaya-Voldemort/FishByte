import time
import json
import os
import random
import tqdm
import helpers


def play_tutorial():
    """
    An interactive tutorial for the FishByte game.
    """
    save_file = "tutorial_save.json"
    fish_data_file = "new_fish.json"

    # --- Setup a clean environment for the tutorial ---
    if os.path.exists(save_file):
        os.remove(save_file)

    # Initial tutorial state
    tutorial_data = {
        "coins": 20,
        "fishing_rod": "Basic",
        "inventory": {
            "fish": []
        },
        "xp": 0
    }
    with open(save_file, "w") as f:
        json.dump(tutorial_data, f, indent=4)

    with open(fish_data_file, "r") as file:
        fish_data = json.load(file)

    print("Welcome to the FishByte tutorial!")
    input("Press Enter to continue...")

    print("\nIn FishByte, you're a fisher trying to make a living.")
    print("You'll catch fish, sell them for coins, and upgrade your gear.")
    input("Press Enter to continue...")

    # --- Help Command ---
    print("\nFirst things first, if you ever get stuck, just type 'help'.")
    print("This will show you a list of all available commands.")
    input("Press Enter to continue...")

    # --- Fishing ---
    print("\nLet's start with the most important command: 'fish'.")
    print("Type 'fish' in the main menu to cast your line.")
    print("When you're fishing, you'll need to be quick! A message will appear on screen telling you to press ENTER.")
    print("The faster you press ENTER, the better your chances of catching a fish.")
    print("Let's try it now!")
    input("Press Enter to cast your line...")

    print("Pulling in the fish...")
    time.sleep(random.uniform(0.5, 2.0))

    print("!!! PRESS ENTER NOW !!!")
    start_time = time.time()
    input()
    end_time = time.time()

    reaction_time = end_time - start_time

    print(f"Nice! You reacted in {reaction_time:.2f}s.")

    print("Fish caught!")
    # Hardcode a fish for the tutorial to ensure consistency
    chosen_fish = ('Discus', 'Bronze', {'value': 40})
    print(f"You caught a: {chosen_fish[0]} ({chosen_fish[1]})")
    helpers.edit_json(save_file, "inventory.fish", chosen_fish[0] + " (" + chosen_fish[1] + ")")
    with open(save_file, "r") as file:
        data = json.load(file)
    current_xp = data.get("xp", 0)
    helpers.edit_json(save_file, "xp", current_xp + 10)

    # --- Gallery ---
    print("\nNice catch! Every new fish you catch is added to your gallery.")
    print("Use the 'gallery' command to see all the unique fish you've discovered.")
    input("Press Enter to continue...")

    print("\nLet's check your gallery now.")
    input("Press Enter to view your gallery...")

    gallery_data = {chosen_fish[0]: {"Bronze": 1}}
    print("\n--- TUTORIAL GALLERY ---")
    for fish_name, rarities in gallery_data.items():
        print(f"{fish_name}:")
        for rarity, count in rarities.items():
            print(f"  - {rarity}: Caught {count} time(s)")
    print("------------------------")
    input("Press Enter to continue...")


    input("Press Enter to continue...")

    # --- Inventory ---
    print("\nAfter you've caught some fish, you'll want to see what you have.")
    print("Use the 'view inventory' command to see your fish, coins, and fishing rod.")
    print("Let's look at your inventory now.")
    input("Press Enter to continue...")

    with open(save_file, "r") as file:
        data = json.load(file)
    print("\n--- TUTORIAL INVENTORY ---")
    print(f"Coins: {data.get('coins', 0)}")
    print(f"Fishing Rod: {data.get('fishing_rod', 'Basic')}")
    print(f"XP: {data.get('xp', 0)}")
    print("Your fish inventory:")
    for i, fish in enumerate(data.get("inventory", {}).get("fish", []), start=1):
        print(f"{i}. {fish}")
    print("--------------------------")
    input("Press Enter to continue...")

    # --- Selling ---
    print("\nNow that you have some fish, you can sell them for coins.")
    print("Use the 'sell fish' command to sell your fish.")
    print("Let's sell the fish you just caught.")
    input("Press Enter to sell your fish...")

    with open(save_file, "r") as file:
        data = json.load(file)

    fish_to_sell = data["inventory"]["fish"][0]
    fish_name = fish_to_sell[:fish_to_sell.index("(")].strip()
    fish_rarity = fish_to_sell[fish_to_sell.index("(") + 1:fish_to_sell.index(")")]

    fish_value = 0
    for fish in fish_data["fish"]:
        if fish["name"] == fish_name:
            rarity_info = fish["rarities"].get(fish_rarity)
            if rarity_info:
                fish_value = rarity_info["value"]
                break

    coins = data.get("coins", 0)
    coins += fish_value
    helpers.edit_json(save_file, "coins", coins)
    helpers.edit_json(save_file, "inventory.fish", [])

    print(f"You sold {fish_to_sell} for {fish_value} coins!")
    print(f"You now have {coins} coins.")
    input("Press Enter to continue...")

    # --- Stats ---
    print("\nWant to see how you're doing? Use the 'stats' command.")
    print("This will show you your total fish caught and your most valuable catch.")
    input("Press Enter to see your stats...")

    with open(save_file, "r") as file:
        data = json.load(file)
    print("\n--- TUTORIAL STATS ---")
    print(f"Total fish caught: 1")
    print(f"Most valuable fish: {fish_name} ({fish_value} coins)")
    print("----------------------")
    input("Press Enter to continue...")

    # --- Shop ---
    print("\nWhat do you do with all those coins? Buy better gear, of course!")
    print("Use the 'enter shop' command to see what's for sale.")
    print("A better fishing rod will help you catch rarer and more valuable fish.")
    print("Let's visit the shop. We've given you some extra coins for this tutorial.")
    input("Press Enter to enter the shop...")

    # Give player enough coins to buy a rod for the tutorial
    helpers.edit_json(save_file, "coins", 10000)
    with open(save_file, "r") as file:
        data = json.load(file)
    print(f"You have {data.get('coins', 0)} coins.")

    shop_items = {
        "1": {"name": "Basic Fishing Rod", "cost": 10000, "rod": "Basic"},
        "2": {"name": "Advanced Fishing Rod", "cost": 50000, "rod": "Advanced"},
        "3": {"name": "Elite Fishing Rod", "cost": 100000, "rod": "Elite"},
    }
    print("\n--- TUTORIAL SHOP ---")
    for key, item in shop_items.items():
        print(f"{key}. {item['name']} - {item['cost']} coins")
    print("---------------------")

    print("\nLet's buy the 'Basic Fishing Rod'.")
    input("Press Enter to purchase...")

    item_cost = shop_items["1"]["cost"]
    item_rod = shop_items["1"]["rod"]

    helpers.edit_json(save_file, "coins", data.get("coins", 0) - item_cost)
    helpers.edit_json(save_file, "fishing_rod", item_rod)

    print("You have purchased the Basic Fishing Rod!")
    with open(save_file, "r") as file:
        data = json.load(file)
    print(f"You now have {data.get('coins', 0)} coins and a {data.get('fishing_rod')} rod.")
    input("Press Enter to continue...")

    # --- Saving ---
    print("\nDon't forget to save your progress!")
    print("Use the 'save game' command to save your inventory, coins, and gear.")
    print("In the main game, you need to do this manually.")
    input("Press Enter to continue...")

    # --- Exit ---
    print("\nAnd finally, when you're done playing, use the 'exit' command.")
    input("Press Enter to continue...")

    print("\nThat's it for the tutorial! You're ready to start your fishing adventure.")
    print("Good luck and have fun!")
    time.sleep(2)

    # --- Cleanup ---
    if os.path.exists(save_file):
        os.remove(save_file)
