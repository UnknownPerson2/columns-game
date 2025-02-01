# columns-game
# Project Setup Instructions

Follow these steps to clone the repository and run the project.

## Prerequisites
- **Git**: Install from [git-scm.com](https://git-scm.com/).
- **Python 3.x**: Install from [python.org](https://www.python.org/).

## Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/UnknownPerson2/columns-game.git
   cd columns-game
2. **Run the game**
   ```bash
   python3 view.oy

## Game Controls

Use the following keys to play the game:

- **Left Arrow (←)**: Move the faller to the left.
- **Right Arrow (→)**: Move the faller to the right.
- **Spacebar**: Rotate the faller.
- **Automatic Drop**: The faller will automatically drop down over time.

### How to Play
1. Use the **arrow keys** to position the faller.
2. Press the **spacebar** to rotate the faller and align it with matching jewels.
3. Match **3 or more jewels** of the same color (horizontally, vertically, or diagonally) to clear them.
4. The game ends when a faller cannot fully enter the grid.

### Game States
- **AIR**: The faller is still falling.
- **LANDED**: The faller has landed but can still be moved or rotated.
- **FROZEN**: The faller is frozen in place and can no longer be moved.
- **MATCH**: Jewels that are part of a match will be highlighted and cleared.

---
