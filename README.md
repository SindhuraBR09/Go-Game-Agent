# Go-Game-Agent

Developed as a Go-game agent, this AI system employs the Min-Max and Alpha-Beta pruning algorithms as its learning mechanisms. It has been crafted to excel in a modified version of the Go game known as Go-5x5 or Little-Go, featuring a compact board with dimensions reduced to 5x5. This adept agent showcases its prowess by competing against a spectrum of AI opponents, ranging from rudimentary to advanced.

Game Synopsis:
Go, renowned as an abstract strategy board game, pits two players, namely Black and White, against each other. The primary objective is to secure more territory than the adversary. In this variant, Little-Go, the game adheres to simplified principles:

Players: 
* Two participants, Black and White, partake in the game.
* Board: The Go board comprises an intersecting grid of horizontal and vertical lines. Although the traditional board measures 19x19, the current rendition confines itself to a 5x5 grid.
* Points: Intersections formed by the grid lines are referred to as points, encompassing those at the corners and edges. The game unfolds exclusively on these points, disregarding the squares.
* Stones: Black employs black stones, while White employs white stones.

The game's fundamental course is straightforward:

* It initiates with an empty board.
* Players take turns depositing stones on the board, one stone per turn.
* Any unoccupied point can be chosen for placement, adhering to the "KO" and "no-suicide" rules.
* Once positioned, a stone remains fixed and can solely be removed if captured.
* The entire gameplay of Go (Little-Go) revolves around two cardinal rules: Liberty (No-Suicide) and KO.

Input and Output:
Input data is drawn from "input.txt" located in the working directory and follows this structure:

Line 1: A numeric value, either "1" or "2," designating your chosen color (Black=1, White=2).
Lines 2 to 6: A description of the prior state of the game board, consisting of 5 rows with 5 values each. This represents the state after your preceding move. (Black=1, White=2, Unoccupied=0)
Lines 7 to 11: A depiction of the present state of the game board, mirroring 5 rows with 5 values each. This reflects the state after your opponent's most recent move. (Black=1, White=2, Unoccupied=0)

The output is saved as "output.txt" in the current working directory. Placing a stone is indicated by two integers, denoted as i and j (e.g., "2,3"), with no intervening whitespace. In cases where the agent opts not to make a move, the output file should contain "PASS" in uppercase letters.
