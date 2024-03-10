import cv2
import time
from grid_utils import create_grid, print_grid, update_grid, find_cells_with_symbol
from minesweeper_utils import press_button, read_image, calculate_next_clicks

# Define the mode (EASY, MIDDLE, HARD)
mode = "HARD"

# Start Game by pressing in the middle of the game canvas
if mode == "EASY":
    COLS = 10
    ROWS = 8
    CELL_WIDTH_HEIGHT = 45
    PADDING = 2
    BOARD_WIDTH = 450
    BOARD_HEIGHT = 360
elif mode == "MIDDLE":
    COLS = 18
    ROWS = 14
    CELL_WIDTH_HEIGHT = 30
    PADDING = 2
    BOARD_WIDTH = 540
    BOARD_HEIGHT = 420
elif mode == "HARD":
    COLS = 24
    ROWS = 20
    CELL_WIDTH_HEIGHT = 25
    PADDING = 2
    BOARD_WIDTH = 600
    BOARD_HEIGHT = 500

GRID = create_grid(ROWS, COLS, CELL_WIDTH_HEIGHT, CELL_WIDTH_HEIGHT, PADDING)
press_button(BOARD_WIDTH / 2, BOARD_HEIGHT / 2, "left")
prev_green_cells = COLS * ROWS
first_turn = True

for i in range(100):
    if first_turn: 
        time.sleep(1)
        first_turn = False
    else :
        time.sleep(1)
    board_screenshot = read_image(BOARD_WIDTH, BOARD_HEIGHT)        
    update_grid(GRID, board_screenshot)
    green_cells = find_cells_with_symbol(GRID, 'G')
    
    if (len(green_cells) == 0): 
        break
    
    if (len(green_cells) == prev_green_cells): 
        cell = GRID[green_cells[0]]
        print('RANDOM CLICK')
        press_button(cell['click_position_x'], cell['click_position_y'], 'left')
    
    prev_green_cells = len(green_cells)
    
    calculate_next_clicks(GRID)
   
    print(i)
    print_grid(GRID)
    
    

cv2.waitKey(0)
cv2.destroyAllWindows()