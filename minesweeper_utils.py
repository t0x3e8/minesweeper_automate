import mss
import pyautogui
from PIL import Image

# Top left corner of board MineSweeper game
MOUSE_X, MOUSE_Y = pyautogui.position()

def read_image(board_width, board_height) -> Image:
    """
    Reads the current screen and returns an Image object.
    """
    left, top, width, height = MOUSE_X, MOUSE_Y, board_width, board_height
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
    """
    Calculate the next clicks to be made based on the current state of the grid.
    """
    num_rows, num_cols = grid.shape
     
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
    """
    Clicks on green cells.
    """
    for cell in cells:
        cell_to_click = grid[cell[0], cell[1]]
        press_button(cell_to_click['click_position_x'], cell_to_click['click_position_y'], 'left')
        
def click_flags(grid, cells):
    """
    Marks cells with flags.
    """
    for cell in cells:
        cell_to_click = grid[cell[0], cell[1]]
        cell_to_click['symbol'] = 'F'
        press_button(cell_to_click['click_position_x'], cell_to_click['click_position_y'], 'right')
   
def get_cells_with_symbol(grid, row_index, col_index, symbol):
    """
    Get cells with a specific symbol in the neighborhood of a given cell.
    """
    num_rows, num_cols = grid.shape
    
    neighbors = get_neighbors(row_index, col_index, num_rows, num_cols)
    green_cells = [(r, c) for r, c in neighbors if grid[r, c]['symbol'] == symbol]
    return green_cells

def get_neighbors(row_index, col_index, num_rows, num_cols):
    """
    Get neighboring cells of a given cell.
    """
    neighbors = []
    for i in range(max(0, row_index - 1), min(num_rows, row_index + 2)):
        for j in range(max(0, col_index - 1), min(num_cols, col_index + 2)):
            if i != row_index or j != col_index:
                neighbors.append((i, j))
    return neighbors
   