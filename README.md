# Pasyans Solitaire
A solitaire-like game played in a shell.

Also known as **пасьянс** (*solitaire* in Russian), it's originally a minigame within [EXAPUNKS by Zachtronics](http://www.zachtronics.com/exapunks/). Pasyans is a simple way to kill time and something I wanted to be able to play in a separate window.

### Rules

1. Numbered cards are stacked by **alternating color** and **decreasing value**, and can be moved together as a stack of any size.
2. Face cards are stacked **by suit** in **any order**, and can also be moved as a stack.
3. To win, sort the dealt cards into four completed stacks of numbered cards and four completed stacks of face cards.
4. The furthest right cell is called the **free cell** and can store a single card of any type.

### Commands
+ **Move**: Used to move a single card or a stack from a source cell to a destination cell.

   Ex. `move 1 2`, `move 4 F`, `mv 6 9`  
   
+ **Win**: Used when the player believes they have won, remakes the board if so.

   Ex. `win`
   
+ **Exit**: Used to end the game. Prompts the player to confirm yes before quiting.

   Ex. `exit`
