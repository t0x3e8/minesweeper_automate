import cv2
import time
from grid_utils import create_grid, print_grid, update_grid
from minesweeper_utils import press_button, read_image, calculate_next_clicks

# Define the mode (EASY, MIDDLE, HARD)
mode = "MIDDLE"

# Start Game by pressing in the middle of the game canvas
if mode == "EASY":
    GRID = create_grid(8, 10, 45, 45, 2)
    BOARD_WIDTH, BOARD_HEIGHT = 450, 360
elif mode == "MIDDLE":
    GRID = create_grid(14, 18, 30, 30, 2)
    BOARD_WIDTH, BOARD_HEIGHT = 540, 420
elif mode == "HARD":
    GRID = create_grid(20, 24, 25, 25, 2)
    BOARD_WIDTH, BOARD_HEIGHT = 600, 500

press_button(BOARD_WIDTH / 2, BOARD_HEIGHT / 2, "left")

for i in range(100):
    time.sleep(1)
    board_screenshot = read_image(BOARD_WIDTH, BOARD_HEIGHT )
    update_grid(GRID, board_screenshot)
    calculate_next_clicks(GRID)
    print_grid(GRID)
    print(i)

cv2.waitKey(0)
cv2.destroyAllWindows()