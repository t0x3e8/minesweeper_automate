import numpy as np
from PIL import Image
import pytesseract
import cv2

GREEN_THRESHOLD = 1.1

def create_grid(rows, cols, cell_width, cell_height, padding):
    dtype = [
        ('region', 'i4', (4,)),
        ('padded_region', 'i4', (4,)),
        ('symbol', 'U10'),
        ('check', bool),
        ('click_position_x', int),
        ('click_position_y', int)
    ]
    grid = np.zeros((rows, cols), dtype=dtype)

    for row_index in range(rows):
        for col_index in range(cols):
            # Calculate the region for the current cell
            left = col_index * cell_width
            right = left + cell_width
            top = row_index * cell_height
            bottom = top + cell_height
            region = np.array([left, right, top, bottom])

            # Calculate the padded region
            padded_left = left + padding
            padded_right = right - padding
            padded_top = top + padding
            padded_bottom = bottom - padding
            padded_region = np.array([padded_left, padded_right, padded_top, padded_bottom])

            grid[row_index, col_index]['region'] = region
            grid[row_index, col_index]['padded_region'] = padded_region
            grid[row_index, col_index]['symbol'] = 'G'
            grid[row_index, col_index]['click_position_x'] = (left + right) // 2
            grid[row_index, col_index]['click_position_y'] = (top + bottom) // 2

    return grid

def print_grid(grid: np.ndarray) -> None:
    """
    Print the game grid based on the current screenshot.
    """
    num_rows, num_cols = grid.shape
    for row_index in range(num_rows):
        row_string = ''
        for col_index in range(num_cols):
            cell = grid[row_index, col_index]
            row_string += str(cell['symbol']) + ' '
        print(row_string)


def is_green(region_cell) -> bool:
    """
    Checks if a pixel is green based on a threshold.
    """
    region_array = np.array(region_cell)
    pixels = region_array.reshape(-1, 3)
    unique_pixels, counts = np.unique(pixels, axis=0, return_counts=True)
    unique_pixels_count_dict = {tuple(pixel): count for pixel, count in zip(unique_pixels, counts)}
    top_dominant_pixel = max(unique_pixels_count_dict, key=unique_pixels_count_dict.get)

    r, g, b = top_dominant_pixel
    return g > r * GREEN_THRESHOLD and g > b * GREEN_THRESHOLD

def update_grid(grid: np.ndarray, screenshot_img: Image) -> None:
    """
    Updates the game grid based on the current screenshot.
    """
    num_rows, num_cols = grid.shape
    for row_index in range(num_rows):
        for col_index in range(num_cols):
            cell = grid[row_index, col_index]

            if cell['symbol'] == 'G':
                region = cell['padded_region']
                region_tuple = (region[0], region[2], region[1], region[3])
                cell_image = screenshot_img.crop(region_tuple)
                # cell_image.save(f"{row_index}-{col_index}.png")
                
                ocr_text = OCR_image(cell_image)
                if ocr_text:
                    try:
                        num = int(ocr_text[0])
                        cell['symbol'] = num
                        # region_cell.save(f"{row_index}-{col_index}.png")
                        # print(f"OCR result for cell [{row_index}, {col_index}]: {num}")
                    except ValueError:
                        pass
                elif is_green(cell_image):
                    cell['symbol'] = 'G'
                else:
                    cell['symbol'] = 'X'

def OCR_image(cell_image): 
    gray_cell = cell_image.convert("L")
    gray_image_np = np.array(gray_cell)
    _, binary_image = cv2.threshold(gray_image_np, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    binary_image_pil = Image.fromarray(binary_image)
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=123456789'
    ocr_text = pytesseract.image_to_string(binary_image_pil, config=custom_config).split()

    return ocr_text
                