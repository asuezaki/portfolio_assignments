# sudoku.py
# Andrew Suezaki
# ===================================================
# Python implementation of sudoku with a verification algorithm.
# Note: Easy puzzle with few steps was used for testing/grading purposes
# ===================================================

class Sudoku:
    """
    Represents the game Sudoku
    """

    def __init__(self):
        """
        Initializes game board and solution board
        citation: hard coded puzzle instance is a modified sample sudoku board and solution taken from
        https://www.sudokuessentials.com/support-files/sudoku-easy-1.pdf
        """
        self.board = [[8, 4, 6, 9, 3, 7, 1, 0, 2],  # puzzle starting point
                      [3, 0, 9, 6, 2, 5, 8, 4, 7],
                      [7, 5, 2, 1, 8, 0, 9, 6, 3],
                      [2, 8, 5, 0, 1, 3, 6, 9, 4],
                      [4, 6, 3, 8, 5, 9, 2, 7, 0],
                      [9, 7, 0, 2, 4, 6, 0, 8, 5],
                      [1, 2, 7, 5, 9, 8, 4, 0, 6],
                      [0, 3, 8, 4, 7, 1, 5, 2, 9],
                      [5, 9, 4, 0, 6, 2, 7, 1, 8]]
        self.solution = [[8, 4, 6, 9, 3, 7, 1, 5, 2],  # puzzle solution
                         [3, 1, 9, 6, 2, 5, 8, 4, 7],
                         [7, 5, 2, 1, 8, 4, 9, 6, 3],
                         [2, 8, 5, 7, 1, 3, 6, 9, 4],
                         [4, 6, 3, 8, 5, 9, 2, 7, 1],
                         [9, 7, 1, 2, 4, 6, 3, 8, 5],
                         [1, 2, 7, 5, 9, 8, 4, 3, 6],
                         [6, 3, 8, 4, 7, 1, 5, 2, 9],
                         [5, 9, 4, 3, 6, 2, 7, 1, 8]]
        self.test = [[8, 4, 6, 9, 3, 7, 1, 5, 2],  # board for testing purposes
                     [3, 1, 9, 6, 2, 5, 8, 4, 7],
                     [7, 5, 2, 1, 8, 4, 9, 6, 3],
                     [2, 8, 5, 7, 1, 3, 6, 9, 4],
                     [4, 6, 3, 8, 5, 9, 2, 7, 3],
                     [9, 7, 1, 2, 4, 6, 3, 8, 5],
                     [1, 2, 7, 5, 9, 8, 4, 3, 6],
                     [6, 3, 8, 4, 7, 1, 5, 2, 9],
                     [5, 9, 4, 3, 6, 2, 7, 1, 8]]
        self.moves = 10  # counts number of moves left until board is full
        self.return_board()  # displays board at the start
        print("Welcome to Sudoku.")
        print("The goal is to fill the cells so that each row and each column are distinctly numbered from 1 to 9")
        print("Rows and columns are numbered from 1-9 (ex. row 1 column 1 has value 8)")
        print("Cells to be filled are marked with a 0")
        # print(self.checktest())
        self.prompt()

    def return_board(self):
        """
        Helper function to print the current state of the board in the terminal.
        Citation: Modified from base code printsudoku function from
        https://towardsdatascience.com/solve-sudokus-automatically-4032b2203b64
        """
        print("---------------------")  # horizontal dividers
        for i in range(len(self.board)):    # looping through board
            line = ""
            if i == 3 or i == 6:            # adding dividers every 3 rows
                print("---------------------")
            for p in range(len(self.board[i])): # looping through board
                if p == 3 or p == 6:        # adding dividers every 3 columns
                    line += "| "  # vertical dividers
                line += str(self.board[i][p]) + " "
            print(line)
        print("---------------------")
        print("Remaining moves: " + str(self.moves))    # prints number of moves remaining

    def reset_board(self):
        """
        Function to reset the board/game
        """
        self.board = [[8, 4, 6, 9, 3, 7, 1, 0, 2],  # puzzle starting point
                      [3, 0, 9, 6, 2, 5, 8, 4, 7],
                      [7, 5, 2, 1, 8, 0, 9, 6, 3],
                      [2, 8, 5, 0, 1, 3, 6, 9, 4],
                      [4, 6, 3, 8, 5, 9, 2, 7, 0],
                      [9, 7, 0, 2, 4, 6, 0, 8, 5],
                      [1, 2, 7, 5, 9, 8, 4, 0, 6],
                      [0, 3, 8, 4, 7, 1, 5, 2, 9],
                      [5, 9, 4, 0, 6, 2, 7, 1, 8]]
        self.moves = 10
        self.return_board()
        return self.prompt()

    def prompt(self):
        """
        Function to prompt user for input
        """
        if self.moves == 0:  # checking if board is full
            print("No more available moves. Checking your puzzle...")
            if self.check():  # calls function to check user solution
                print("Puzzle complete! Congrats!")  # indicates if puzzle is correct or not and then asks
                again = input("Play again? Enter Y or N: ")  # if user wants to play again
                if again == "Y":
                    return self.reset_board()  # calls function to reset board to play again
                else:
                    return print("Thank you for playing!")  # otherwise ends program
            else:
                reset = input("Puzzle incorrect. Try again? Enter Y or N: ")
                if reset == "Y":
                    return self.reset_board()
                else:
                    return print("Thank you for playing!")
        val1 = int(input("Please enter your desired row: "))  # user input for desired row
        if val1 < 1 or val1 > 9:  # user input validation
            print("Error: You did not enter a valid row from 1-9")
            return self.prompt()
        val2 = int(input("Please enter your desired column: "))  # user input for desired column
        if val2 < 1 or val2 > 9:  # user input validation
            print("Error: You did not enter a valid column from 1-9")
            return self.prompt()
        if self.board[val1 - 1][val2 - 1] != 0:  # checking that a valid cell was entered
            print("Error: Only select empty cells represented by a 0")
            return self.prompt()
        val3 = int(input("Please enter a value: "))  # user input for desired value
        if val3 <= 0 or val3 > 9:  # checking that number is valid
            print("Error: Value must be between 1-9 Try Again")
            return self.prompt()
        return self.make_move(val1, val2, val3)  # uses user input to add the value into the board

    def make_move(self, row, col, val):
        """
        Function to make moves on the board
        """
        self.board[row - 1][col - 1] = val  # places user input into the board
        self.moves -= 1  # reduces number of remaining moves
        self.return_board()  # prints board to show results
        return self.prompt()  # prompts user for next input

    def check(self):
        """
        Verifies user solution against puzzle solution by comparing each cell in each column in a for loop
        """
        for i in range(len(self.board) - 1):  # for loop through each row
            if self.board[i] != self.solution[i]:    # comparing each row of user input with each row of the solution
                return False                        # stops and returns False if a row does not match
        return True                                 # if all rows match, returns True

    def checktest(self):
        """
        Static testing method for check function. Ignore this
        """
        for i in range(len(self.test) - 1):  # for loop through each row
            if self.test[i] != self.solution[i]:    # comparing each row against the solution
                return False
        return True


Sudoku()
