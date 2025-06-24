# FishByte

## Description

FishByte is a text-based fishing game written in Python. It's a passion project born from a love of fishing and classic text-based RPGs. The game is currently in its early stages, but the foundation is in place for a much larger and more feature-rich experience.

## What's New (June 21, 2025)

*   **Tutorial:** A new tutorial has been added to help new players learn the basics of the game.
*   **The Shop is Open!** You can now spend your hard-earned coins on new fishing rods.
*   **New Fish!** A variety of new fish have been added to the game.

## Devlog (June 21, 2025)

I've been working on making the game more accessible for new players. To that end, I've added a comprehensive tutorial that walks players through the basic mechanics of the game. This should make it easier for newcomers to get started and understand the core gameplay loop. I'm hoping this will improve the overall player experience and encourage more people to stick with the game. I've also been squashing some bugs and tweaking the balancing of the fish rarities.

## Gameplay

The core gameplay loop is simple:

1.  **Fish:** Use the `fish` command to cast your line and catch a variety of fish.
2.  **Sell Fish:** Sell your catches to earn coins.
3.  **View Inventory:** Check your inventory to see your fish, coins, and other items.
4.  **Enter Shop:** Use your coins to buy better fishing rods and other equipment.
5.  **Save Game:** Save your progress.
6.  **Exit:** Exit the game.
7.  **Play Tutorial:** Learn the basics of the game.

## The Shop

You can now access the shop by typing `shop` or `4` in the main menu. Here, you can purchase new fishing rods that will allow you to catch rarer and more valuable fish.

## The Fish Database

One of the things I'm most proud of in this project is the fish database. The `new_fish.json` file contains all the data for the fish in the game, including their names, rarities, values, and catch rates. I have a passion for creating a unique and diverse set of fish, and I've handcrafted the entire database without the use of AI. I've recently added a bunch of new fish to the game, so there's more to discover than ever before!

## AI Assistance

While the fish database is 100% human-made, I have used AI for code assistance in other areas of the project. For example, the `fish` function in `helpers.py`, which determines which fish is caught based on a weighted random choice, was developed with the help of an AI assistant. I've also used AI for general assistance with debugging and code optimization. However, the rest of the core logic of the game was coded by hand.

## Future Plans

My ultimate goal for FishByte is to develop it into a full-fledged game with a graphical user interface (GUI). This text-based version is the first step in that journey, and I'm excited to continue building on it.

## How to Play

To play FishByte, you'll need to have Python and Git installed on your computer. Follow these steps to get started:

1.  **Clone the Repository**
    
    Open your terminal or command prompt and run the following command to download the game files:
    ```bash
    git clone https://github.com/Papaya-Voldemort/FishByte.git
    ```

2.  **Navigate to the Project Directory**
    
    Change your current directory to the newly created `FishByte` folder:
    ```bash
    cd FishByte
    ```

3.  **Install Required Dependencies**
    
    Install the necessary Python packages by running:
    ```bash
    pip install -r requirements.txt
    ```
    > **Note for macOS users:** If the above command doesn't work, you may need to use `pip3` instead:
    > ```bash
    > pip3 install -r requirements.txt
    > ```

4.  **Run the Game**
    
    You're all set! Start the game with the following command:
    ```bash
    python main.py
    ```
    > **Note for macOS users:** You may need to use `python3` instead:
    > ```bash
    > python3 main.py
    > ```
