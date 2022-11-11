# from math import trunc
# from tempfile import _TemporaryFileWrapper
# from flask import Flask
from flask import Flask, render_template, request
import jyserver.Flask as jsf
import minesweeper



app = Flask(__name__)

@jsf.use(app)
class App:
    def __init__(self):
        '''
        A function that initialises variables when the window is loaded.
        :variables:-
        :tileId - Stores the value of tile pressed.
        :tilePressed - boolean value to check if a tile is pressed.
        :number_colors - list of hexagonal colors for each number 1-8
        '''
        self.tileId = ""
        self.tilePressed = False
        self.number_colors =  ['#3498db', '#2ecc71', '#e74c3c', '#9b59b6', '#f1c40f', '#1abc9c', '#34495e', '#7f8c8d',];
        
    def getid(self,id):
        '''
        Function that is called when tile is pressed.
        :params:-
        :id - id of tile pressed
        :variables:-
        :gameOver - boolean to check if game is over or not.
        :num - Stores the value from the backend for the tile clicked.
        '''
        if self.gameOver == False:
            self.tileId = str(self.js.document.getElementById(id).id)
            self.js.document.getElementById('count').innerHTML = self.tileId
            # print("Checking class list contains")
            # print(self.js.document.getElementById(id).classList.contains('tile--checked'))

            if self.js.document.getElementById(id).classList.contains('tile--checked')==True:
                print("True if block in getid")
            else:
            # if tile is checked don't do 
            # otherwise check the tiles
                # print("Faalse if block in getid")
                self.js.document.getElementById(id).classList.add('tile--checked')
                self.num = self.b1.getTileNum(int(self.tileId[0]),int(self.tileId[-1]))

                if self.num == "*":
                    self.js.document.getElementById(id).classList.add('tile--bomb')
                    self.js.document.getElementById(id).innerHTML = "💥"
                elif self.num == "0":
                    self.js.document.getElementById(id).innerHTML = ""
                else:
                    self.js.document.getElementById(id).innerHTML = self.num
                    self.js.document.getElementById(id).style.color = self.number_colors[int(self.num) - 1]

                # self.js.document.getElementById('board').innerHTML = str(self.js.document.getElementById('board').innerHTML)+ "Calling from getid"
                # self.js.document.getElementById('board').innerHTML = self.b1. (self.tileId[0],self.tileId[-1])
                self.tilePressed = True
                # print(self.tileId)
    

    def endGame(self, safe):
        '''
        Function that is called at the end of the game.
        :params:-
        :safe - boolean that checks if bomb is pressed or not. 
        '''
        if safe: # We WON 
            self.js.document.getElementById('endscreen').innerHTML = '🎉CONGRATULATIONS✌😁 '
        else:
            for bomb in self.b1.bombs_list:
                self.getid(bomb)
            self.js.document.getElementById('endscreen').innerHTML = '😊 BETTER LUCK NEXT TIME 😊'
        
        self.gameOver = True
        self.js.document.getElementById('endscreen').classList.add('show')

    # Onloading, we initalised board
    def init_board(self):
        '''
        Function that is called when html loaded
        :variables:-
        :gameOver - boolean to check if game is over or not.
        :b1 - stores an object of class Board from minesweeper.py
        :row - stores the row value of tile pressed.
        :col - stores the column value of tile pressed.
        ''' 
        # self.js.document.getElementById('board').innerHTML = "WINDOW LOADED"
        self.gameOver = False
        self.b1 = minesweeper.Board(10,10)
        # self.dummy(self.b1,self.tileId[0],self.tileId[-1])

        safe = True
        while len(self.b1.dug) < self.b1.dim_size ** 2 - self.b1.num_bombs:
            # print("Not safe")
            # self.js.document.getElementById('board').innerHTML = "Safe to pLay"
            if not self.tilePressed:
                # print(self.tilePressed)
                continue
            
           
            # print(self.tilePressed)
            
            self.tilePressed = False
            
            row,col = int(self.tileId[0]), int(self.tileId[-1]) 
            # if row < 0 or row >= self.b1.dim_size or col < 0 or col >= self.b1.dim_size:
            #     print("Invalid location. Try again.")
            #     continue


            safe = self.b1.dig(row, col)
            # self.js.document.getElementById('board').innerHTML = "PLEASE WAIT"
            print(self.b1.dug)
            for tile in self.b1.dug:
                self.getid(tile)

                
            if not safe:
               break # (game over rip)
            print(self.b1) # Printing Board
            # print("Ready to play")
            # self.js.document.getElementById('board').innerHTML = "Please Wait"
                
                
        # 2 ways to end loop, lets check which one
        if safe:
            print("CONGRATULATIONS!!!! YOU ARE VICTORIOUS!")
            self.endGame(safe)
        else:
            print("SORRY GAME OVER :(")
            self.endGame(safe)
            # let's reveal the whole board!
            self.b1.dug = [(r,c) for r in range(self.b1.dim_size) for c in range(self.b1.dim_size)]
            print(self.b1)
            # break


    


@app.route('/frontpage')
def example():
    ''''
    Flask function that returns rendered html frontpage on route ..../frontpage.
    '''
    return render_template('frontpage.html')

@app.route('/finalGame')
def finalGame():
    '''
    Flask function that returns rendered html gamepage on route ..../finalGame.
    :variables:-
    :name - Stores the value of the user input from frontpage and is passed to gamepage.
    '''
    name = request.args.get('name')
    return App.render(render_template('finalGamepage.html', usrname = name))

# Only run if file is called by itself.
if __name__ == '__main__':
    app.run(debug=True)
