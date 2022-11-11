import random
import re

# Creating a board object to represent the minesweeper game
class Board:
    def __init__(self, dim_size, num_bombs):
        '''
        Creates a board, initialise dimension of the board and number of bombs in it.
        :params:-
        :dim_size - dimension of board.
        :num_bombs - Number of bombs on board.
        :variables:-
        :bombs_list - list of location of bombs.
        :board - list of values for the board.
        :dug - set of id of tiles dug.
        '''
        
        self.dim_size = dim_size
        self.num_bombs = num_bombs
        self.bombs_list = []

        self.board = self.make_new_board() # plant the bombs
        self.assign_values_to_board()

        self.dug = set() # initialize a set to keep track of which locations we've uncovered


    def make_new_board(self):
        '''
        Construct a new board based on the dim size and num bombs. Returns the list of values through board.
        :variables:-
        :bombs_planted - Number of bombs planted.
        :loc - Stores the random location of tile for bomb to be planted.
        :row - Stores the row value of tile for the bomb.
        :col - Stores the column value of tile for the bomb.

        '''
        
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)] # generate a new board
        # [[None, None, ..., None],
        #  [None, None, ..., None],
        #  [...                  ],
        #  [None, None, ..., None]]
        
        # planting the bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2 - 1) 
            row = loc // self.dim_size  
            col = loc % self.dim_size  

            if board[row][col] == '*':
                continue

            board[row][col] = '*' 
            self.bombs_list.append((row,col))
            bombs_planted += 1

        return board


    def assign_values_to_board(self):
        '''
        Possible number of bombs around a tile. Assigning a number 0-8 to a tile which represents it's neighbouring bombs.
        '''
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)


    def get_num_neighboring_bombs(self, row, col):
        '''
        Returns the number which pops up in the tile representing the number of bombs around it.
        :variables:-
        :num_neighboring_bombs - Stores any number between 0-8 depending on surrounding bomb tiles.
        '''
        # top left: (row-1, col-1)
        # top middle: (row-1, col)
        # top right: (row-1, col+1)
        # left: (row, col-1)
        # right: (row, col+1)
        # bottom left: (row+1, col-1)
        # bottom middle: (row+1, col)
        # bottom right: (row+1, col+1)

        num_neighboring_bombs = 0
        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if r == row and c == col: # original location
                    continue
                if self.board[r][c] == '*':
                    num_neighboring_bombs += 1

        return num_neighboring_bombs

    def dig(self, row, col):
        '''
        Returns true if tile dug is not bomb, false if tile dug is bomb
        3 scenarios.
        1) dig a bomb - game over 
        2) dig a tile with a number - opens that particular tile 
        3) dig an empty tile - it will recursively dig it's neighbouring tiles until all tiles are next to a bomb.
        :params:-
        :row - Row value of tile id.
        :col - Column value of tile id.
        '''
        
        self.dug.add((row, col)) 
        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True

        for r in range(max(0, row-1), min(self.dim_size-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dim_size-1, col+1)+1):
                if (r, c) in self.dug:
                    continue 
                self.dig(r, c)

        return True
        
    def getTileNum(self,row,col):
        '''
        Clicking on a particular tile it returns the position of that tile (row,column) to the backend.
        :params:-
        :row - Row value of tile id.
        :col - Column value of tile id.

        '''
        return str(self.board[row][col])

    def __str__(self):
        '''
        This shows the user interactions with the board on the backend, returns a string that shows the board to the player when object is printed.
        :variables:-
        :visible_board - list of values of all tiles of board
        :string_rep - String representation of the board which is returned.
        :widths - 
        :columns -
        :indices - 
        :indices_row - 
        :cells -
        '''
        # first let's create a new array that represents what the user would see
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row,col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '
        
        # put this together in a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep

# play the game
    def play(self,x,y, dim_size=10, num_bombs=10):
        '''
        When called, runs the minesweeper game in the backend. Input is taken from the command-line. Only called when needed to see working in backend.
        '''
        # Step 1: create the board and plant the bombs
        # Step 2: show the user the board and ask for where they want to dig
        # Step 3a: if location is a bomb, show game over message
        # Step 3b: if location is not a bomb, dig recursively until each square is at least
        #          next to a bomb
        # Step 4: repeat steps 2 and 3a/b until there are no more places to dig -> VICTORY!

        safe = True 

        while len(self.dug) < self.dim_size ** 2 - num_bombs:
            print(self)
            # print([x,y])
            if x=="" or y=="":
                continue
            # user_input = re.split(',(\\s)*', input("Where would you like to dig? Input as row,col: "))  # '0, 3'
            # row, col = int(user_input[0]), int(user_input[-1])
            row,col = int(x), int(y)
            if row < 0 or row >= self.dim_size or col < 0 or col >= dim_size:
                print("Invalid location. Try again.")
                continue

            # if it's valid, we dig
            safe = self.dig(row, col)
            if not safe:
                break # (game over rip)
            
            

        # 2 ways to end loop
        if safe:
            print("CONGRATULATIONS!!!! YOU ARE VICTORIOUS!")
        else:
            print("SORRY GAME OVER :(")
            # Revealing whole board!
            self.dug = [(r,c) for r in range(self.dim_size) for c in range(self.dim_size)]
            print(self)

# if __name__ == '__main__': # good practice :)
#     play()
