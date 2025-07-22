#!/usr/bin/env python3
"""
FishByte Demo - Self-Contained Version
A fishing game where you catch fish, manage inventory, and upgrade equipment.
This demo version runs independently without external files.
"""

import random
import time
import sys

# Optional colorama for colored text (graceful fallback if not available)
try:
    import colorama
    from colorama import Fore, Style
    colorama.init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False

class FishByteDemo:
    def __init__(self):
        self.money = 100
        self.fishing_rod = "Basic"
        self.inventory = []
        self.total_fish_caught = 0
        self.total_money_earned = 0

        # Embedded fish data (simplified version)
        self.fish_data = {
            "fish": [
                {
                    "name": "Goldfish",
                    "rarities": {
                        "Bronze": {"value": 10, "catch_rate": {"Basic": 1000, "Advanced": 250, "Elite": 0}},
                        "Silver": {"value": 30, "catch_rate": {"Basic": 200, "Advanced": 400, "Elite": 50}},
                        "Gold": {"value": 100, "catch_rate": {"Basic": 20, "Advanced": 150, "Elite": 300}},
                        "Platinum": {"value": 250, "catch_rate": {"Basic": 2, "Advanced": 50, "Elite": 100}},
                        "Diamond": {"value": 750, "catch_rate": {"Basic": 0, "Advanced": 1, "Elite": 25}},
                        "Mythic": {"value": 1250, "catch_rate": {"Basic": 0, "Advanced": 0, "Elite": 5}}
                    }
                },
                {
                    "name": "Betta",
                    "rarities": {
                        "Bronze": {"value": 25, "catch_rate": {"Basic": 900, "Advanced": 300, "Elite": 0}},
                        "Silver": {"value": 75, "catch_rate": {"Basic": 150, "Advanced": 450, "Elite": 50}},
                        "Gold": {"value": 250, "catch_rate": {"Basic": 15, "Advanced": 100, "Elite": 400}},
                        "Platinum": {"value": 750, "catch_rate": {"Basic": 1, "Advanced": 25, "Elite": 75}},
                        "Diamond": {"value": 1500, "catch_rate": {"Basic": 0, "Advanced": 1, "Elite": 25}},
                        "Mythic": {"value": 2000, "catch_rate": {"Basic": 0, "Advanced": 0, "Elite": 7}}
                    }
                },
                {
                    "name": "Guppy",
                    "rarities": {
                        "Bronze": {"value": 25, "catch_rate": {"Basic": 900, "Advanced": 300, "Elite": 0}},
                        "Silver": {"value": 75, "catch_rate": {"Basic": 150, "Advanced": 450, "Elite": 50}},
                        "Gold": {"value": 150, "catch_rate": {"Basic": 15, "Advanced": 100, "Elite": 400}},
                        "Platinum": {"value": 300, "catch_rate": {"Basic": 1, "Advanced": 25, "Elite": 75}},
                        "Diamond": {"value": 600, "catch_rate": {"Basic": 0, "Advanced": 1, "Elite": 25}},
                        "Mythic": {"value": 1200, "catch_rate": {"Basic": 0, "Advanced": 0, "Elite": 7}}
                    }
                },
                {
                    "name": "Angelfish",
                    "rarities": {
                        "Bronze": {"value": 30, "catch_rate": {"Basic": 850, "Advanced": 150, "Elite": 0}},
                        "Silver": {"value": 75, "catch_rate": {"Basic": 100, "Advanced": 250, "Elite": 25}},
                        "Gold": {"value": 275, "catch_rate": {"Basic": 10, "Advanced": 75, "Elite": 200}},
                        "Platinum": {"value": 575, "catch_rate": {"Basic": 1, "Advanced": 25, "Elite": 50}},
                        "Diamond": {"value": 1150, "catch_rate": {"Basic": 0, "Advanced": 1, "Elite": 15}},
                        "Mythic": {"value": 2300, "catch_rate": {"Basic": 0, "Advanced": 0, "Elite": 3}}
                    }
                },
                {
                    "name": "Bass",
                    "rarities": {
                        "Bronze": {"value": 50, "catch_rate": {"Basic": 600, "Advanced": 100, "Elite": 0}},
                        "Silver": {"value": 150, "catch_rate": {"Basic": 50, "Advanced": 200, "Elite": 25}},
                        "Gold": {"value": 450, "catch_rate": {"Basic": 5, "Advanced": 50, "Elite": 150}},
                        "Platinum": {"value": 900, "catch_rate": {"Basic": 0, "Advanced": 15, "Elite": 40}},
                        "Diamond": {"value": 1800, "catch_rate": {"Basic": 0, "Advanced": 1, "Elite": 10}},
                        "Mythic": {"value": 3600, "catch_rate": {"Basic": 0, "Advanced": 0, "Elite": 2}}
                    }
                },
                {
                    "name": "Shark",
                    "rarities": {
                        "Bronze": {"value": 200, "catch_rate": {"Basic": 100, "Advanced": 50, "Elite": 0}},
                        "Silver": {"value": 600, "catch_rate": {"Basic": 10, "Advanced": 100, "Elite": 25}},
                        "Gold": {"value": 1800, "catch_rate": {"Basic": 1, "Advanced": 25, "Elite": 75}},
                        "Platinum": {"value": 3600, "catch_rate": {"Basic": 0, "Advanced": 5, "Elite": 25}},
                        "Diamond": {"value": 7200, "catch_rate": {"Basic": 0, "Advanced": 1, "Elite": 5}},
                        "Mythic": {"value": 14400, "catch_rate": {"Basic": 0, "Advanced": 0, "Elite": 1}}
                    }
                }
            ]
        }

        # Shop items
        self.shop_items = {
            "fishing_rods": {
                "Advanced": {"price": 500, "description": "Better catch rates for rare fish"},
                "Elite": {"price": 2000, "description": "Best catch rates for all fish types"}
            }
        }

    def color_text(self, text, color):
        """Apply color to text if colorama is available, otherwise return plain text."""
        if not COLORAMA_AVAILABLE:
            return text

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

    def fish_catch(self):
        """Simulate catching a fish based on weighted probabilities."""
        weighted_choices = []
        weights = []

        # Collect all fish rarities with their catch rates for the current fishing rod
        for fish in self.fish_data["fish"]:
            for rarity, stats in fish["rarities"].items():
                catch_rate = stats["catch_rate"].get(self.fishing_rod, 0)
                if catch_rate > 0:
                    weighted_choices.append((fish["name"], rarity, stats))
                    weights.append(catch_rate)

        # Use random.choices to pick one based on weights
        if weighted_choices:
            chosen = random.choices(weighted_choices, weights=weights, k=1)[0]
            return chosen
        else:
            return None

    def fishing_animation(self):
        """Simple fishing animation."""
        print(self.color_text("Casting line...", "cyan"))
        time.sleep(0.5)

        for i in range(3):
            print(self.color_text("🎣 Waiting for a bite...", "yellow"))
            time.sleep(0.8)

        print(self.color_text("🐟 Something's biting!", "green"))
        time.sleep(0.5)

    def go_fishing(self):
        """Main fishing function."""
        print(self.color_text("🎣 You cast your line into the water...", "cyan"))
        self.fishing_animation()

        catch = self.fish_catch()
        if catch:
            fish_name, rarity, stats = catch
            value = stats["value"]

            # Add to inventory
            fish_entry = f"{rarity} {fish_name}"
            self.inventory.append(fish_entry)
            self.total_fish_caught += 1

            # Display catch
            rarity_colors = {
                "Bronze": "yellow",
                "Silver": "white",
                "Gold": "yellow",
                "Platinum": "cyan",
                "Diamond": "blue",
                "Mythic": "magenta"
            }

            print(self.color_text(f"🎉 You caught a {rarity} {fish_name}!", rarity_colors.get(rarity, "green")))
            print(self.color_text(f"💰 Value: ${value}", "green"))

        else:
            print(self.color_text("😞 No fish this time... Try again!", "red"))

    def view_inventory(self):
        """Display current inventory."""
        print(self.color_text("🎒 Your Inventory:", "bold"))
        print(self.color_text("=" * 30, "cyan"))

        if not self.inventory:
            print(self.color_text("Your inventory is empty. Go fishing!", "yellow"))
            return

        # Group fish by type for better display
        fish_count = {}
        total_value = 0

        for fish in self.inventory:
            if fish in fish_count:
                fish_count[fish] += 1
            else:
                fish_count[fish] = 1

            # Calculate value
            parts = fish.split()
            if len(parts) >= 2:
                rarity = parts[0]
                name = " ".join(parts[1:])

                # Find fish value
                for fish_data in self.fish_data["fish"]:
                    if fish_data["name"] == name:
                        if rarity in fish_data["rarities"]:
                            total_value += fish_data["rarities"][rarity]["value"]
                        break

        for fish, count in fish_count.items():
            print(self.color_text(f"  {fish} x{count}", "cyan"))

        print(self.color_text("=" * 30, "cyan"))
        print(self.color_text(f"💰 Total Inventory Value: ${total_value}", "green"))

    def sell_fish(self):
        """Sell all fish in inventory."""
        if not self.inventory:
            print(self.color_text("You have no fish to sell!", "red"))
            return

        total_earned = 0
        fish_sold = len(self.inventory)

        for fish in self.inventory:
            parts = fish.split()
            if len(parts) >= 2:
                rarity = parts[0]
                name = " ".join(parts[1:])

                # Find fish value
                for fish_data in self.fish_data["fish"]:
                    if fish_data["name"] == name:
                        if rarity in fish_data["rarities"]:
                            value = fish_data["rarities"][rarity]["value"]
                            total_earned += value
                            self.money += value
                        break

        self.inventory.clear()
        self.total_money_earned += total_earned

        print(self.color_text(f"🐟 Sold {fish_sold} fish for ${total_earned}!", "green"))
        print(self.color_text(f"💰 Total money: ${self.money}", "yellow"))

    def enter_shop(self):
        """Shop interface for buying fishing rods."""
        while True:
            print(self.color_text("\n🏪 Welcome to the Fish Shop!", "bold"))
            print(self.color_text("=" * 35, "cyan"))
            print(self.color_text(f"💰 Your money: ${self.money}", "yellow"))
            print(self.color_text(f"🎣 Current rod: {self.fishing_rod}", "cyan"))
            print()

            print(self.color_text("Available Fishing Rods:", "bold"))

            available_rods = []
            for rod_name, rod_info in self.shop_items["fishing_rods"].items():
                if rod_name != self.fishing_rod:
                    available_rods.append((rod_name, rod_info))
                    print(self.color_text(f"  {len(available_rods)}. {rod_name} - ${rod_info['price']}", "cyan"))
                    print(self.color_text(f"     {rod_info['description']}", "white"))

            if not available_rods:
                print(self.color_text("You already have the best fishing rod!", "green"))
                input(self.color_text("Press Enter to leave shop...", "yellow"))
                break

            print(self.color_text(f"  {len(available_rods) + 1}. Leave shop", "red"))

            try:
                choice = input(self.color_text("\nWhat would you like to buy? ", "yellow"))
                choice_num = int(choice)

                if choice_num == len(available_rods) + 1:
                    break
                elif 1 <= choice_num <= len(available_rods):
                    rod_name, rod_info = available_rods[choice_num - 1]

                    if self.money >= rod_info["price"]:
                        self.money -= rod_info["price"]
                        self.fishing_rod = rod_name
                        print(self.color_text(f"🎉 Purchased {rod_name} fishing rod!", "green"))
                        print(self.color_text(f"💰 Remaining money: ${self.money}", "yellow"))
                    else:
                        print(self.color_text("💸 Not enough money!", "red"))
                else:
                    print(self.color_text("Invalid choice!", "red"))

            except ValueError:
                print(self.color_text("Please enter a valid number!", "red"))

    def show_stats(self):
        """Display player statistics."""
        print(self.color_text("\n📊 Your Statistics:", "bold"))
        print(self.color_text("=" * 25, "cyan"))
        print(self.color_text(f"🐟 Total fish caught: {self.total_fish_caught}", "cyan"))
        print(self.color_text(f"💰 Current money: ${self.money}", "green"))
        print(self.color_text(f"💵 Total money earned: ${self.total_money_earned}", "yellow"))
        print(self.color_text(f"🎣 Current fishing rod: {self.fishing_rod}", "blue"))
        print(self.color_text(f"🎒 Fish in inventory: {len(self.inventory)}", "magenta"))

    def show_tutorial(self):
        """Show basic tutorial."""
        print(self.color_text("\n🎓 FishByte Tutorial", "bold"))
        print(self.color_text("=" * 20, "cyan"))
        print(self.color_text("Welcome to FishByte! Here's how to play:", "yellow"))
        print()
        print(self.color_text("🎣 Fish: Cast your line and catch fish", "cyan"))
        print(self.color_text("🎒 Inventory: View what you've caught", "cyan"))
        print(self.color_text("💰 Sell: Sell your fish for money", "cyan"))
        print(self.color_text("🏪 Shop: Buy better fishing rods", "cyan"))
        print(self.color_text("📊 Stats: View your progress", "cyan"))
        print()
        print(self.color_text("Fish come in different rarities:", "yellow"))
        print(self.color_text("Bronze → Silver → Gold → Platinum → Diamond → Mythic", "white"))
        print(self.color_text("Rarer fish are worth more money!", "green"))
        print()
        print(self.color_text("Better fishing rods help you catch rarer fish!", "yellow"))

    def main_menu(self):
        """Main game loop."""
        print(self.color_text("🐟 Welcome to FishByte Demo! 🐟", "bold"))
        print(self.color_text("A self-contained fishing adventure!", "cyan"))

        while True:
            print(self.color_text("\n" + "=" * 40, "cyan"))
            print(self.color_text("What would you like to do?", "yellow"))
            print(self.color_text("1. 🎣 Go Fishing", "cyan"))
            print(self.color_text("2. 🎒 View Inventory", "cyan"))
            print(self.color_text("3. 💰 Sell Fish", "cyan"))
            print(self.color_text("4. 🏪 Enter Shop", "cyan"))
            print(self.color_text("5. 📊 View Stats", "cyan"))
            print(self.color_text("6. 🎓 Tutorial", "cyan"))
            print(self.color_text("7. 🚪 Exit", "red"))

            choice = input(self.color_text("\nEnter your choice (1-7): ", "yellow")).strip()

            if choice == "1" or choice.lower() == "fish":
                self.go_fishing()
            elif choice == "2" or choice.lower() == "inventory":
                self.view_inventory()
            elif choice == "3" or choice.lower() == "sell":
                self.sell_fish()
            elif choice == "4" or choice.lower() == "shop":
                self.enter_shop()
            elif choice == "5" or choice.lower() == "stats":
                self.show_stats()
            elif choice == "6" or choice.lower() == "tutorial":
                self.show_tutorial()
            elif choice == "7" or choice.lower() == "exit":
                print(self.color_text("🌊 Thanks for playing FishByte Demo! 🌊", "cyan"))
                print(self.color_text("Hope you enjoyed your fishing adventure!", "green"))
                break
            else:
                print(self.color_text("❌ Invalid choice! Please try again.", "red"))

def main():
    """Entry point for the demo."""
    try:
        game = FishByteDemo()
        game.main_menu()
    except KeyboardInterrupt:
        print("\n🌊 Thanks for playing FishByte Demo! 🌊")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please restart the game.")

if __name__ == "__main__":
    main()
