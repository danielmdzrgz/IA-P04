import tkinter as tk
import tkinter.messagebox as msgbox
from pyswip import Prolog
from sudoku import Sudoku


seconds, minutes = 0, 0                 # Variables to store the timer           
prolog = Prolog()                       # Create a Prolog object to use the Prolog database
sudoku = Sudoku(3).difficulty(0.5)      # Create a 3x3 Sudoku board with a difficulty of 0.5, which means that 50% of the cells will be empty


# Function to solve the Sudoku using Prolog logic defined in sudoku.pl
def solve_sudoku(puzzle: list):
    prolog.consult("sudoku.pl")                                                     # Consult the file sudoku.pl where the logic is defined

    for i in range(9):
        for j in range(9):
            puzzle[i][j] = 0 if puzzle[i][j] is None else puzzle[i][j]              # Replace None values with 0

    board = str(puzzle).replace("0", "_")                                           # And replace 0 values with _ to be able to use the Prolog query
    pl_solution = list(prolog.query("L=%s, sudoku(L)" % board, maxresult=1))        # Query the Prolog database to get the solution
    return pl_solution[0]['L']                                                      # Return the solution


# Function to update the timer every second
def update_timer():
    global seconds, minutes                                     # Use the global variable seconds
    seconds += 1                                                # Increment the seconds by 1
    if seconds == 60:
        minutes += 1                                            # Increment the minutes by 1 if seconds is 60
        seconds = 0                                             # Reset the seconds to 0

    timer_label.config(text=f"{minutes:02d}:{seconds:02d}")     # Update the timer label
    root.after(1000, update_timer)                              # Call the function again after 1 second


# Function to add validation to each Entry widget in the Sudoku board
def callback(input):
    if (input.isdigit() and int(input) in range(1, 10)) or input == "":      # If input is a number between 1 and 9 or empty, is valid
        return True
    
    print("LOG: Invalid input -> " + input)                                  # Else, is invalid. Log the input in console and exit
    return False


# Function to check if the input in a cell is valid
def checkIfValid(x: int, y: int):
    if sudoku_board[x][y].get() == "":                                          # Correction of background color if the incorrect input is deleted
        sudoku_board[x][y].config(bg="white")
    elif int(sudoku_board[x][y].get()) != int(solution[x][y]):                  # If the input is not equal to the solution, is invalid and show a warning
        sudoku_board[x][y].config(bg="red")
    else:                                                                       # Else, the input is the same as the solution, is valid
        sudoku_board[x][y].destroy()                                            # Destroy the Entry widget
        sudoku_board[x][y] = tk.Label(frame, text=solution[x][y], width=2)      # Create a Label widget with the solution
        sudoku_board[x][y].grid(row=x, column=y)                                # Place the Label widget in the correct position


# Function to submit the Sudoku
def submitSudoku():
    for i in range(sudoku.height * 3):
        for j in range(sudoku.width * 3):
            if type(sudoku_board[i][j]) != tk.Label:                                # If the cell is not a Label widget, is not finished (Has at least one cell pending to resolve)
                print("LOG: Sudoku submitted but not finished")                     # Log the message in console
                msgbox.showwarning("Sudoku Game", "Sudoku still not finished")      # Show a warning message
                return  

    print("LOG: Sudoku submitted and finished")                                                                         # Else the Sudoku is finished, log the message in console
    msgbox.showinfo("Sudoku Game", "Congratulations, you finished the Sudoku!\nTime: " + timer_label.cget("text"))      # Show a completition message with the time
    root.destroy()                                                                                                      # Destroy the main window (Exit the game)



solution = solve_sudoku(sudoku.board)       # Solve the Sudoku using Prolog logic defined in sudoku.pl

root = tk.Tk()                      # Create the main window
root.title("Sudoku Game")           # Set the title of the window
root.geometry("600x600")            # Set the size of the window

tk.Label(root, text="").pack()                                                    # Empty label to add space
title_label = tk.Label(root, text="Sudoku", font=("Arial Bold", 30)).pack()       # Label with the game's title
tk.Label(root, text="").pack()

timer_label = tk.Label(root, text="00:00")      # Label to show the timer
timer_label.pack()
update_timer()                                  # Start the timer and update it every second            
tk.Label(root, text="").pack()  

frame = tk.Frame(root)        # Create a frame
frame.pack()                  # Pack the frame

canvas = tk.Canvas(frame, width=300, height=300)            # Create a canvas to draw the Sudoku board
canvas.grid(row=0, column=0, columnspan=9, rowspan=9)       # Place the canvas and set the number of rows and columns

for i in range(1, 3):                               # Draw the lines of the Sudoku board
    canvas.create_line(100*i, 0, 100*i, 300)        # Vertical lines
for i in range(1, 3):
    canvas.create_line(0, 100*i, 300, 100*i)        # Horizontal lines

sudoku_board = []                                                                               # Create a list to store the Entry widgets of the Sudoku board 
for i in range(9):
    sudoku_board.append([])
    for j in range(9):
        if sudoku.board[i][j] != 0:                                                             # If the cell is not empty, create a Label widget
            element = tk.Label(frame, text=sudoku.board[i][j], width=2)                         # and set the text to the value of the cell
        else:
            element = tk.Entry(frame, width=2)                                                  # Else, create an Entry widget                      
            element.config(validate="key", validatecommand=(root.register(callback), "%P"))     # and add validation to the input so only numbers between 1 and 9 can be entered
            element.bind("<KeyRelease>", lambda event, x=i, y=j: checkIfValid(x, y))            # Bind the checkIfValid function to the KeyRelease event to check if the input is correct
        element.grid(row=i, column=j)                                                           # Place the Entry/Label widget in the grid
        sudoku_board[i].append(element)                                                         # Add the Entry/Label widget to the list

tk.Label(root, text="").pack()
submit_button = tk.Button(root, text="Submit Sudoku", command=submitSudoku).pack()              # Button to submit the Sudoku
tk.Label(root, text="").pack()
tk.Label(root, text="").pack()
exit_button = tk.Button(root, text="Exit", command=root.destroy).pack()                         # Button to exit the game

root.mainloop()    # Start the main loop