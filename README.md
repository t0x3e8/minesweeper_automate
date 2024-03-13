Minesweeper Bot
This Python script provides a Minesweeper bot capable of automatically playing the game. It utilizes image processing techniques and OCR to analyze the game board and make intelligent decisions about where to click next.

[![Link to demo on youtube](https://i3.ytimg.com/vi/COpXQbb-Ez4/maxresdefault.jpg)](https://youtu.be/COpXQbb-Ez4)

Dependencies
Make sure you have the following dependencies installed:
* numpy
* PIL
* pytesseract
* mss
* pyautogui
* cv2 
You can install these dependencies via pip:
```bash
Copy code
pip install numpy pillow pytesseract mss pyautogui opencv-python-headless
```

You also need to install tesseract from https://github.com/tesseract-ocr/tesseract

Usage
Adjust the mode variable to match the difficulty level of your Minesweeper game (EASY, MIDDLE, or HARD).
Run the script.
Start a Minesweeper game and position the mouse cursor over the top-left corner of the game board.
The bot will automatically detect the game board, read the state of the game, and make moves accordingly.
How It Works
The script works by:

Capturing screenshots of the game board using mss.
Analyzing each cell of the game grid:
Using image processing techniques to identify the color of each cell (green, flagged, or unknown).
Performing OCR on flagged cells to identify the number of adjacent mines.
Deciding the next move based on the state of the game board:
Clicking on green cells if they are safe.
Marking cells with flags if all adjacent mines have been identified.
Making random clicks if no safe moves are available.
Contributing
Contributions are welcome! Feel free to open issues or submit pull requests to improve the functionality or performance of the bot.

Disclaimer
This script is intended for educational purposes only. Use it responsibly and respect the terms of service of the game platform you are playing on.

License
This project is licensed under the MIT License - see the LICENSE file for details.





