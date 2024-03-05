import cv2
import numpy as np
import pygetwindow as gw
import mss
import pyautogui
from PIL import Image
from collections import Counter
import time
from grid_utils import create_grid, print_grid, update_grid

# TODO: this is hard level, easy and medium levels are missing
# w, h = 600, 500
# BOARD_WIDTH, BOARD_HEIGHT = 450, 360 # EASY
# BOARD_WIDTH, BOARD_HEIGHT = 540, 420 # MIDDLE
BOARD_WIDTH, BOARD_HEIGHT = 600, 500
# Top left corner of board MineSweeper game
MOUSE_X, MOUSE_Y = pyautogui.position()

def read_image() -> Image:
    """
    Reads the current screen and returns an Image object.
    """
    left, top, width, height = MOUSE_X, MOUSE_Y, BOARD_WIDTH, BOARD_HEIGHT
    with mss.mss() as sct:
        monitor = {"top": top, "left": left, "width": width, "height": height}
        screenshot = sct.grab(monitor)
    
    return Image.frombytes("RGB", screenshot.size, screenshot.rgb)

def press_button(offset_x: int, offset_y: int, button_name: str) -> None:
    """
    Presses a button on the screen at the specified coordinates.
    """
    target_x = MOUSE_X + offset_x
    target_y = MOUSE_Y + offset_y
    pyautogui.click(x=target_x, y=target_y, button=button_name)

def calculate_next_clicks(grid):
    num_rows, num_cols = grid.shape
     
    # for number in range(1, 9):
    for row_index in range(num_rows):
        for col_index in range(num_cols):
            cell = grid[row_index, col_index]

            if cell['symbol'].isdigit():
                number = int(cell['symbol'])
                g_cells = get_cells_with_symbol(grid, row_index, col_index, 'G')
                f_cells = get_cells_with_symbol(grid, row_index, col_index, 'F')
                
                if number == len(f_cells) and len(g_cells) > 0:
                    click_green(grid, g_cells)
                elif number == len(f_cells) + len(g_cells):
                    click_flags(grid, g_cells)
                    
def click_green(grid, cells):
    for cell in cells:
        cell_to_click = grid[cell[0], cell[1]]
        press_button(cell_to_click['click_position_x'], cell_to_click['click_position_y'], 'left')
        
def click_flags(grid, cells):
    for cell in cells:
        cell_to_click = grid[cell[0], cell[1]]
        cell_to_click['symbol'] = 'F'
        press_button(cell_to_click['click_position_x'], cell_to_click['click_position_y'], 'right')
        

def get_cells_with_symbol(grid, row_index, col_index, symbol):
    num_rows, num_cols = grid.shape
    
    neighbors = get_neighbors(row_index, col_index, num_rows, num_cols)
    green_cells = [(r, c) for r, c in neighbors if grid[r, c]['symbol'] == symbol]
    return green_cells

def get_neighbors(row_index, col_index, num_rows, num_cols):
    neighbors = []
    for i in range(max(0, row_index - 1), min(num_rows, row_index + 2)):
        for j in range(max(0, col_index - 1), min(num_cols, col_index + 2)):
            if i != row_index or j != col_index:
                neighbors.append((i, j))
    return neighbors

# Start Game by pressing in the middle of the game canvas
# GRID = create_grid(8, 10, 45, 45, 2)  # Mode EASY
# GRID = create_grid(14, 18, 30, 30, 2)  # Mode MIDDLE
GRID = create_grid(20, 24, 25, 25, 2)  # Mode HARD
press_button(BOARD_WIDTH / 2, BOARD_HEIGHT / 2, "left")

for i in range(15):
    time.sleep(1)
    # TODO This to be loop
    SCREENSHOT_IMG = read_image()
    update_grid(GRID, SCREENSHOT_IMG)
    calculate_next_clicks(GRID)
    print_grid(GRID)
    print(i)

cv2.waitKey(0)
cv2.destroyAllWindows()
