## Introduction

---

Tower of Hanoi App is a graphical user interface application built using Tkinter in Python. The app visualizes the Tower of Hanoi problem, allowing users to run, pause/resume, take the next step, and reset the animation.

## Features

---

- Automatic animation of Tower of Hanoi problem
- Buttons for controlling the animation: Run, Pause/Resume, Next Step, Reset
- User input for the number of discs
- Colorful representation of discs
- Pegs and background visualization

## Installation

---

To run the application, make sure you have Python installed. Clone the repository and run the following command:

```bash
python app.py
```

## How to Use

---

1. Enter the number of discs in the input box (recommended range: 1-16).
2. Set the animation speed using the speed input box (recommended range: 1-10).
3. Click the "Run" button to start the automatic animation.
4. Use the "Pause/Resume" button to pause or resume the animation.
5. Click "Next" to move the animation one step forward manually.
6. Press "Reset" to reset the animation with the current disc number and speed.
7. To quit the application, click the "Quit" button.

## Known Issues

---

- **Issue 1: If the number of discs is greater than 22, the program may not function correctly.**

  - Resolution: Input a number of discs below or equal to 22. If an error occurs, click "Reset" to reset the discs.

- **Issue 2: If the speed setting is greater than 10, there may be flickering and changes in disc shapes.**
  - Resolution: Enter a speed value below 10. Inputting excessively large values may result in unexpected outcomes.
