# Python Battleship

###### This is the final project for CPE/EE/AAI 551, Engineering Programming: Python.
This is the Battleship game built using Python. A GUI is implemented through the use of the PyGame and Tkinter Packages.

## Concept
1. Create a GUI Battleship board/grid.
2. Allow the player to select which cells they wish to place their ships in before the game starts
	- I've gone with the standard rules where players place 5 ships of various sizes on a 10 by 10 grid
	- The ships are of sizes 2, 3, 3, 4, and 5.
3. Once the game starts, the player gets to take turns with the CPU firing missiles onto the opposing board, attempting to hit and destroy the opponent's ships.
	- If a player lands a hit, they get to fire another missile.
4. Game ends when all of a player's ships have been destroyed.
5. Implement a multiplayer version that allows players to play against each other rather than against the CPU.

## Video Demo
A quick demo of the base game can be found [here](https://youtu.be/tUbF7VPHI1A)

## Steps
### 1. Generating the GUI in PyGame
The first step was to figure out how to use the PyGame package and its modules to generate a GUI and draw the battleship boards onto it. Since this was my first time using PyGame, I was not familiar with how it works and have to look into the package's documentations as well as look for some video tutorials showcasing it. 

The main question that I had at the start of this project was "How am I going to implement the different aspects of Battleship?" I was not sure how I wanted the game to look and how I wanted the user to perform the actions required to play the game. After looking through several PyGame tutorials and featured games, I came across a version of [PyGame Battleship](https://github.com/igor-bond16/Battle_Ship_Game/tree/master/Battle%20Ship%20Complete) created by Japanese user [@Bond Igor](https://github.com/igor-bond16). He showcased his version of Battleship in a [YouTube video](https://www.youtube.com/watch?v=jZ3F4kNnxM4) and I really loved his idea of using PyGame to draw the two boards and display the current status of the game, then use a separate Tkinter window filled with buttons to perform actions. Therefore, I decided to adopt his implementation of Battleship and use his source code as an example for my game. After going through his source code, I noticed that it was not coded using Object-oriented programming (OOP) and his version of Battleship strayed from the standard rules and was missing several key features of the game. Therefore I am only going to refer to his game for the implementation of it using PyGame and Tkinter.

To generate the GUI in PyGame, I had to first initialize PyGame, as well as the variables/settings that I am going to use for the PyGame window. Then, I created the `Board` class which includes the functions to draw the board and its axis titles within the PyGame window. At this point, the game looks like this:

![initial_board.PNG](./Images/initial_board.PNG)

### 2. Player Ship Generation (Letting the user place ships on the board)
The next step was to work on generating ships onto the PyGame board. Remember that in Igor's version, the user was able to click buttons on an external Tkinter window to determine where the player's ships will be placed. Following his approach, I created a `Ships` class that initializes a Tkinter instance and have it generate a block of buttons, one for each cell on the board. The user will be able to click on the cell they want their ship to be on and the button will turn green. If they change their mind, they can click the button again to undo it. The idea is that these buttons will append the cell index into an array, which will determine the cells that get filled in on the game board. At this point, the game looks like this:

![initial_player_ships.gif](./Images/initial_player_ships.gif)

I have not yet constrained the cells that the player is able to select (since they should only be able to select the cells for their 5 ships), but I will implement that at a later step.

### 3. Enemy Ship Generation (Single-Player)
Currently, the game is single-player, therefore the enemy (in this case, CPU), must be able to generate their 5 ships randomly. Since I had already set up the method to draw the ships onto the board, it was just a matter of randomly generating the cell indexes that will be appended to the array to be drawn. To do this, a main loop will run until all ships are generated. First, I had to first randomize the the orientation of each ship, either horizontal or veritcal. Then, based on the orientation, a two integers will be randomly generated, which will represent the coordinate of the ship on the board. A loop will run based on the size of the ship to check if any of the cells of the ship collides with another ship. If it does, skip this ship. After the loop ends, all 5 ships of various sizes should be placed. To see this work, I had the game temporarily draw this on the enemy's board:

![initial_enemy_ships.gif](./Images/initial_enemy_ships.gif)

### 4. Attacking Mechanic
The next step, now that both sides are able to generate their ships, is to allow both sides to attack each other. To allow the player to attack, a new Tkinter window will pop up that allows the player to select which cell it wants to attack. Once clicked, the button will be disabled and the button as well as the enemy's board will show the cell as either black or red, depending on if a ship was hit or not. If the player hits a ship, they get to go again. Otherwise, the enemy gets to take a shot and also gets to go again should they land a hit. The CPU will attack randomly until they hit a ship. At this point the game looks like this:

![initial_attack.gif](./Images/initial_attack.gif)

###### Note: The enemy ships are still displayed for testing purposes.

Once the CPU hit a ship, it is only logical to check the cells around it and attack until it misses, where then it should check the other direction until the ship is destroyed. For now, the CPU only attacks randomly. This will be implemented at a later step.

### 5. Win Condition!
The final step for the base game would be to check for the win condition. This means, once either side's ships are all destroyed, the game ends and the player either wins or loses. To do this, I created a `check_win_condition` function which will get called after every successful hit. It checks if there are any remaining indices left inside both user's `selected` array (a.k.a. if there are any ship cells still alive). If either user's `selected` array is empty, then all of their ships have been destroyed and the opponent is declared the winner. A text that would either be "You Lose..." or "You Win!" is rendered and is displayed on the game window and all of the Tkinter buttons will be disabled. The game now looks like this:

![initial_win_lose.gif](./Images/initial_win_lose.gif)

### 6. Ship Placement Constraints... sort of
At this point, the base game is complete... if the player follows the standard rules. The ship placement process has not yet been constrained, therefore the player is allowed to place however many ship cells, wherever they please. We need to fix that.

Unfortunately, while I was trying to implement this, I ran into an issue. Given any array of 17 selected cells (2+3+3+4+5 = 17), how do I determine whether it is a valid Battleship board or not? After trying several methods, I am only able to *partially* constrain the player's ship placement. The first test was obviously whether there are 17 values in the `selected` array. If there are not, then the board is definitely invalid. However, this does not check if the ships are placed in lines, rather only if ANY 17 cells are selected. This meant the player could just have 17 cells laid out across the 10x10 grid in anyway they want. Not what we want. 

The next test was to follow the enemy ship generation method from step 3 above. I passed through the array of selected cells and available ships left and try to check off the available ships left as I searched through the selected cells. Unfortunately, this only worked under ideal conditions. If several ships are placed next to each other, it would fail to detect them as separate ships. Also, since all this sees is a 1D array of values, as long as the values are consecutive, it would be treated as a horizontal ship. This meant that cells 8, 9, 10, and 11 were selected, it would be seen as a ship of length 4 even though on the grid half of it wraps over to the next row.

In the end, to save time, I decided to use a different approach for ship placement. Since players typically try to randomize the way they place their ships, I will disable the whole grid of buttons and create one new button called "Randomize." Essentially, I will borrow the enemy ships generation method I wrote earlier and apply that for the player's ships too. The player will be able to randomize their ship placement as many times as they want until they get a layout that they like. This method ensures that the ship placement is valid while still giving the player some freedom in their ship placement:

![random_ship_placement.gif](./Images/random_ship_placement.gif)

### 7. Improve CPU Attack Mechanic -- ***POSTPONED***
The only thing left to comeplete this single-player Battleship game would be to improve the CPU's attack mechanic. As mentioned earlier, as of right now, the CPU always fires missiles randomly. Logically, once it lands a hit, it should check the surrounding cells for connected ship cells. Only once the ship is destroyed should it try to find another one randomly.

On second thought, the aforementioned idea would be flawed with my setup and there will be a lot of extra steps required to make it work. Since I am using indices for random selection AND cell checking, the CPU has no way of knowing whether it is at an edge (or near an edge), making it easy for the next attempted hit/series of hits to be out of bounds or wrapped around to the next/previous row on the board. While this is a slightly better method to playing Battleship, it is still not optimal.

After doing a quick search, I came across two key videos, one talking about the methods behind playing Battleship ([The Battleship Algorithm by Vsauce2](https://www.youtube.com/watch?v=LbALFZoRrw8)) and the other about implementing these methods ([Demolishing Battleship Board Game Using Probability - Building a AI in Python by Challenging Luck](https://www.youtube.com/watch?v=aCj8Ajc1yUU)). They suggest an algorithm which builds a board of probabilities based on where ships can be placed. Based the on hits/misses already performed, it determines where ships of all sizes can be places. Areas of less misses would have a higher probability of containing a ship as opposed to areas where there are already tons of misses. For more details, I suggest watching the two short videos linked above.

###### NOTE: Due to time-constraints, I have decided to POSTPONE this step for the time being.

### 8. Playing Against Real People! (Multiplayer) -- ***POSTPONED***
I originally wanted to implement a Client-Server network that would run a local server and allow users to join rooms where they can play, but due to time-constraints, I have decided to POSTPONE this step for the time being.