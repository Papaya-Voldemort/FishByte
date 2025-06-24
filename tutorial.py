import time
import json
import os
import random
import helpers


def play_tutorial():
    """
    An interactive tutorial for the FishByte game.
    """
    save_file = "tutorial_save.json"
    fish_data_file = "fish/new_fish.json"

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

    print(helpers.color_text("Welcome to the FishByte tutorial!", "bold"))
    input("Press Enter to continue...")

    print(helpers.color_text("\nIn FishByte, you're a fisher trying to make a living.", "cyan"))
    print(helpers.color_text("You'll catch fish, sell them for coins, and upgrade your gear.", "cyan"))
    input("Press Enter to continue...")

    # --- Help Command ---
    print(helpers.color_text("\nFirst things first, if you ever get stuck, just type 'help'.", "yellow"))
    print(helpers.color_text("This will show you a list of all available commands.", "yellow"))
    input("Press Enter to continue...")

    # --- Fishing ---
    print(helpers.color_text("\nLet's start with the most important command: 'fish'.", "green"))
    print(helpers.color_text("Type 'fish' in the main menu to see the fishing locations.", "green"))
    print(helpers.color_text("The 'Home Pond' is always available, but you'll need to buy tickets to fish in other locations.", "green"))
    print(helpers.color_text("Let's try fishing in the Home Pond now!", "bold"))
    input("Press Enter to continue...")


    print(helpers.color_text("Pulling in the fish...", "yellow"))
    time.sleep(random.uniform(0.5, 2.0))

    print(helpers.color_text("!!! PRESS ENTER NOW !!!", "red"))
    start_time = time.time()
    input()
    end_time = time.time()

    reaction_time = end_time - start_time

    print(helpers.color_text(f"Nice! You reacted in {reaction_time:.2f}s.", "green"))

    print(helpers.color_text("Fish caught!", "green"))
    # Hardcode a fish for the tutorial to ensure consistency
    chosen_fish = ('Discus', 'Bronze', {'value': 40})
    print(f"You caught a: {helpers.color_text(chosen_fish[0], 'blue')} ({helpers.color_text(chosen_fish[1], 'purple')})")
    helpers.edit_json(save_file, "inventory.fish", chosen_fish[0] + " (" + chosen_fish[1] + ")")
    with open(save_file, "r") as file:
        data = json.load(file)
    current_xp = data.get("xp", 0)
    helpers.edit_json(save_file, "xp", current_xp + 10)

    # --- Gallery ---
    print(helpers.color_text("\nNice catch! Every new fish you catch is added to your gallery.", "cyan"))
    print(helpers.color_text("Use the 'gallery' command to see all the unique fish you've discovered.", "cyan"))
    input("Press Enter to continue...")

    print(helpers.color_text("\nLet's check your gallery now.", "yellow"))
    input("Press Enter to view your gallery...")

    gallery_data = {chosen_fish[0]: {"Bronze": 1}}
    print(helpers.color_text("\n--- TUTORIAL GALLERY ---", "bold"))
    for fish_name, rarities in gallery_data.items():
        print(f"{fish_name}:")
        for rarity, count in rarities.items():
            print(f"  - {rarity}: Caught {count} time(s)")
    print(helpers.color_text("------------------------", "bold"))
    input("Press Enter to continue...")


    input("Press Enter to continue...")

    # --- Inventory ---
    print(helpers.color_text("\nAfter you've caught some fish, you'll want to see what you have.", "cyan"))
    print(helpers.color_text("Use the 'view inventory' command to see your fish, coins, and fishing rod.", "cyan"))
    print(helpers.color_text("Let's look at your inventory now.", "yellow"))
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
    print("You can buy better fishing rods and tickets to new fishing locations.")
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
    ticket_prices = {
        "river": 50,
        "lake": 100,
        "shallow_ocean": 200,
        "deep_ocean": 500
    }
    print("\n--- TUTORIAL SHOP ---")
    print("--- Fishing Rods ---")
    for key, item in shop_items.items():
        print(f"{key}. {item['name']} - {item['cost']} coins")
    print("--- Tickets ---")
    print(f"4. River Ticket - {ticket_prices['river']} coins")
    print(f"5. Lake Ticket - {ticket_prices['lake']} coins")
    print("--------------------")


    print("\nLet's buy the 'River Ticket'.")
    input("Press Enter to purchase...")

    item_cost = ticket_prices["river"]

    helpers.edit_json(save_file, "coins", data.get("coins", 0) - item_cost)
    helpers.edit_json(save_file, "tickets.river", True)

    print("You have purchased the River Ticket!")
    with open(save_file, "r") as file:
        data = json.load(file)
    print(f"You now have {data.get('coins', 0)} coins and can fish in the river.")
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
