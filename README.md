# Minesweeper-using-Flask
Recreated the retro game Minesweeper using Flask.

How to play:

●	Start by clicking on any random tile.

●	The number inside each tile denotes the number of mines that surround the opened tile. For example: If the number on an opened tile is two, then there are two mines that are in close proximity to the opened tile i.e two mines can be in any of the eight tiles surrounding it.

●	Win the game by opening all tiles without stepping on a mine. Step on a mine and you lose the game.

●	You can replay the game if win or lose. Detailed instructions are there on the page.



How to start the game:

●	Take a git clone of the repository.

●	Open cmd with python loaded in the environment or you can open anaconda prompt and go to the location of the cloned folder.

●	Once in the cloned location, in the terminal type 'python test.py' and hit enter to run it

●	Once it's run it will give you a local address, copy the local address and paste it on any web browser. Add '/frontpage' after the address in the URL bar and then you should get the login page to the game, which is hosted locally on your machine.




File Structure:

●	static folder - contains files such as images that are used on the HTML and css files that are used on different elements of the HTML 

●	template folder   - contains all HTML files that are used in the project.

●	minesweeper.py  - contains the algorithm and working of the game

●	test.py  - contains the Flask code and this is the main file to run.






