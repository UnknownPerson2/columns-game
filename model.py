# logic

import random

ROWS = 13
COLS = 16
COLORS = ['1', '2', '3', '4', '5', '6', '7']
FALLER_LENGTH = 3

class InvalidGameError(Exception):
    ''' raised whenever invalid game parameters are given '''
    pass

class InvalidMoveError(Exception):
    ''' raised whenever an invalid move is made '''
    pass

class GameOverError(Exception):
    ''' raised whenever an attempt is made to move after the game is over '''
    pass

class ColumnGame():
    def __init__(self):
        # check # of rows and cols
        self._rows = ROWS
        self._cols = COLS
        
        # initalize game state
        self._fields = [[' ' for _ in range(self._cols)] for _ in range(self._rows + FALLER_LENGTH - 1)]
        self._faller = []
        self._faller_position = [[0, 0, 0], 0]
        self._game_over = False

    def get_rows(self):
        return self._rows
    
    def get_cols(self):
        return self._cols
    
    def is_game_over(self) -> bool:
        ''' checks if game is over '''
        # faller landed but cannot be displayed entirely in field
        rows, col = self._faller_position
        if rows[2] != self._rows + FALLER_LENGTH - 2:
            if 'FROZEN' in self._fields[rows[2] + 1][col] and 'FROZEN' in self._fields[1][col]:
                self._game_over = True
        return self._game_over
    
    def _new_faller(self) -> None:
        ''' creates a new faller '''
        # check if there's a current faller
        if self._faller and not self._is_frozen():
            return
            
        # get colors
        colors = []
        colors += (str(random.randint(1, 7)) for _ in range(3))
        self._faller = colors

        # get col
        cols = self._find_all_available_column()
        col = int(random.choice(cols))
        self._faller_position = [[0, 1, 2], col]

        # if faller matches by itself
        temp = set(colors)
        if len(temp) == 1:
            self._faller = []
            self._faller_position = [[0, 0, 0], 0]

        if col is None:
            raise GameOverError()
        
        # only bottommost of its 3 jewels should be visible at its creation
        if 'FROZEN' in self._fields[3][col]:
            self._fields[0][col] = f"LANDED {colors[0]}"
            self._fields[1][col] = f"LANDED {colors[1]}"
            self._fields[2][col] = f"LANDED {colors[2]}"
        else:
            self._fields[0][col] = f"AIR {colors[0]}"
            self._fields[1][col] = f"AIR {colors[1]}"
            self._fields[2][col] = f"AIR {colors[2]}"

    def _find_all_available_column(self) -> list[int]:
        ''' returns all columns that can fit a faller '''
        cols = []
        for col in range(self._cols):
            if self._fields[0][col] == ' ' and self._fields[1][col] == ' ' and self._fields[2][col] == ' ':
                cols.append(col)
        return cols

    def _handle_time(self) -> None:
        ''' simulate passage of time: fall, land, freeze '''
        # should always drop all jewels
        self._drop_jewels()

        # get bottom row for every column
        bottom = {}
        for col in range(self._cols):
            for row in range(self._rows + 1, 1, -1):
                # frozen
                if 'FROZEN' in self._fields[row][col]:
                        bottom[col] = row - 1
                else:
                    # floor
                    if row == len(self._fields) - 1:
                        bottom[col] = row

        # check if faller is at bottom then check status to convert if needed
        rows, col = self._faller_position
        for row in rows:
            cell = self._fields[row][col]
            # faller land when they can't be moved down any further
            if 'AIR' in cell and bottom[col] == row:
                self._change_status('LANDED')
            # faller freeze at next empty cmd after they have landed
            elif 'LANDED' in cell and bottom[col] == row:
                self._change_status('FROZEN')
                self._faller = []
                self._faller_position = [[0, 0, 0], 0]

    def _drop_jewels(self, type: str = 'ONE') -> None:
        ''' fill ALL holes OR drop ONE at a time'''
        rows = len(self._fields)
        cols = len(self._fields[0])
        
        if type == 'ONE':
            result = self._fields
            if self._faller:

                faller_rows, faller_col = self._faller_position

                can_fall = True

                # makes sure faller fits
                for row in faller_rows:
                    if not (row + 1 < rows):
                        can_fall = False

                # checks if spot below faller is empty
                try:
                    if not (result[faller_rows[-1] + 1][faller_col] == ' '):
                        can_fall = False
                except IndexError:
                    pass

                # drop
                if can_fall:
                    for row in reversed(faller_rows):
                        result[row + 1][faller_col] = self._fields[row][faller_col]
                        result[row][faller_col] = ' '
                    faller_rows = [row + 1 for row in faller_rows]
                # can't drop
                else:
                    for row in faller_rows:
                        result[row][faller_col] = self._fields[row][faller_col]

                # update faller's position
                self._faller_position = [faller_rows, faller_col]
                
        # drop all
        elif type == 'AFTER':
            result = self._fields
            for row in range(len(result) - 2, -1, -1):
                for col in range(len(result[0])):
                    if result[row + 1][col] == ' ' and result[row][col] != ' ' and row not in self._faller_position[0]:
                        result[row + 1][col] = result[row][col]
                        result[row][col] = ' '

        self._fields = result

    def _change_status(self, status: str) -> None:
        ''' change status of faller (air, landed, frozen) '''
        # count for keeping track of color (starts at top)
        count = 0
        for row in self._faller_position[0]:
            col = self._faller_position[1]
            self._fields[row][col] = f'{status} {self._faller[count]}'
            count += 1

    def _rotate_faller(self) -> None:
        ''' rotate jewels in the faller '''
        if self._faller:
            # make sure not frozen
            if not self._is_frozen():
                rows, col = self._faller_position

                # update field
                temp = [self._fields[row][col] for row in rows]
                self._fields[rows[0]][col] = temp[2]
                self._fields[rows[1]][col] = temp[0]
                self._fields[rows[2]][col] = temp[1]
                
                # update faller
                temp = [row[:] for row in self._faller]
                self._faller[0] = temp[2]
                self._faller[1] = temp[0]
                self._faller[2] = temp[1]

            else:
                raise InvalidMoveError()
        else:
            raise InvalidMoveError()

    def _move_faller(self, direction: int) -> None:
        ''' move faller left or right if possible '''
        if self._faller:
            # make sure not frozen
            if not self._is_frozen():
                rows, col = self._faller_position

                # get new coord
                new_col = col + direction

                # check direction
                if not (0 <= new_col < self._cols):
                    raise InvalidMoveError()
                for row in rows:
                    if self._fields[row][new_col] != ' ':
                        return
                    
                # moves
                for row in rows:
                    if 0 <= row < self._rows + FALLER_LENGTH and self._fields[row][new_col] == ' ':
                        # check if faller is landed then changes to air unless it's at the bottom
                        if 'LANDED' in self._fields[row][col]:
                            self._fields[row][new_col] = f"AIR {self._fields[row][col][-1]}"
                            self._fields[row][col] = ' '
                            self._faller_position[1] = new_col
                        else:
                            self._fields[row][new_col] = self._fields[row][col]
                            self._fields[row][col] = ' '
                            self._faller_position[1] = new_col
                    else:
                        raise InvalidMoveError()
            else:
                raise InvalidMoveError()
        else:
            raise InvalidMoveError()

    def _match(self) -> None:
        ''' matches all jewels possible, should change field '''
        rows = len(self._fields)
        cols = len(self._fields[0])

        while True:
            matching_jewels_location = []
            for row in range(rows):
                for col in range(cols):
                    jewel = self._fields[row][col]
                    if jewel == ' ':
                        continue

                    # check for horizontal match (left -> right)
                    if col <= cols - 3 and self._fields[row][col + 1] == jewel and self._fields[row][col + 2] == jewel:
                        matching_jewels_location += [(row, col), (row, col + 1), (row, col + 2)]

                    # check for vertical match (up -> down)
                    if row <= rows - 3 and self._fields[row + 1][col] == jewel and self._fields[row + 2][col] == jewel:
                        matching_jewels_location += [(row, col), (row + 1, col), (row + 2, col)]

                    # check diagonal (top left -> down right)
                    if row <= rows - 3 and col <= cols - 3 and self._fields[row + 1][col + 1] == jewel and self._fields[row + 2][col + 2] == jewel:
                        matching_jewels_location += [(row, col), (row + 1, col + 1), (row + 2, col + 2)]

                    # check diagonally (top right -> down left)
                    if row <= rows - 3 and col >= 2 and self._fields[row + 1][col - 1] == jewel and self._fields[row + 2][col - 2] == jewel:
                        matching_jewels_location += [(row, col), (row + 1, col - 1), (row + 2, col - 2)]

            # switches status of every match
            for match in matching_jewels_location[:]:
                row, col = match
                self._fields[row][col] = f'MATCH {self._fields[row][col][-1]}'
                matching_jewels_location.remove((match))

            # no more matches
            if len(matching_jewels_location) == 0:
                break

    def _delete_matches(self) -> None:
        ''' removes all matches, should only be called if there are matches '''
        for row in range(self._rows + FALLER_LENGTH - 1):
            for col in range(self._cols):
                if 'MATCH' in self._fields[row][col]:
                    self._fields[row][col] = ' '
                    self._drop_jewels('AFTER')

    def _is_frozen(self) -> bool:
        ''' checks if faller is frozen '''
        if not self._faller:
            return
        rows, col = self._faller_position
        for row in rows:
            if 0 <= row < self._rows and 'FROZEN' in self._fields[row][col]:
                return True
        return False