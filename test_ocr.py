from PIL import Image
import pytesseract
import cv2
import numpy as np

# Open the image
image = Image.open("6-8.png")
image.show()

# Convert the image to grayscale
gray_image = image.convert("L")
gray_image.show()

# Convert the PIL image to numpy array
gray_image_np = np.array(gray_image)

# Apply binary thresholding using Otsu's method
_, binary_image = cv2.threshold(gray_image_np, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

# Convert the binary image back to PIL format
binary_image_pil = Image.fromarray(binary_image)
binary_image_pil.show()

# Perform OCR using pytesseract
custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=123456789'
ocr_text = pytesseract.image_to_string(binary_image_pil, config=custom_config).split()
print(ocr_text)
