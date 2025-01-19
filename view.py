# user interface

import model
import pygame

_INITIAL_WIDTH = 600
_INITIAL_HEIGHT = 600
_BACKGROUND_COLOR = pygame.Color(0, 0, 0)

def get_color_from_value(value: int):
    if value == 1:
        return (255, 102, 102)
    elif value == 2:
        return (255, 178, 102)
    elif value == 3:
        return (225, 255, 102)
    elif value == 4:
        return (102, 255, 178)
    elif value == 5:
        return (102, 178, 255)
    elif value == 6:
        return (102, 102, 255)
    elif value == 7:
        return (255, 102, 255)

class ColumnsGame:
    def __init__(self):
        self._running = True
        self._game = model.ColumnGame()
        self._state = self._game._fields[2:]
        
        self._surface_width = _INITIAL_WIDTH
        self._surface_height = _INITIAL_HEIGHT

        self.last_faller_move = pygame.time.get_ticks()
        self.faller_move_interval = 500

    def run(self) -> None:
        pygame.init()
        pygame.mixer.init()

        self._surface = pygame.display.set_mode((self._surface_width, self._surface_height), pygame.RESIZABLE)

        clock = pygame.time.Clock()

        while self._running: 
            clock.tick(10)

            self._handle_events()
            self._redraw()

            pygame.time.delay(100)

        self._game_over_display()

        pygame.quit()

    def _handle_events(self) -> None:
        ''' handles quitting, resizing, creating new faller, handling user-inputs, dropping faller, matching '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._end_game()
            elif event.type == pygame.VIDEORESIZE:
                self._surface_width, self._surface_height = event.w, event.h
                self._surface = pygame.display.set_mode((self._surface_width, self._surface_height), pygame.RESIZABLE)

        try:
            self._game._new_faller()

            self._handle_keys()

            self._game._handle_time()

            self._game._match()

            if self._game.is_game_over():
                self._end_game()

        except model.GameOverError:
            self._end_game()

    def _handle_keys(self) -> None:
        ''' handles keys: left, right, rotate '''
        try:
            keys = pygame.key.get_pressed()
            # moves left
            if keys[pygame.K_LEFT]:
                self._game._move_faller(-1)
            # moves right
            if keys[pygame.K_RIGHT]:
                self._game._move_faller(1)
            # rotates
            if keys[pygame.K_SPACE]:
                self._game._rotate_faller()
        except model.InvalidMoveError:
            pass

    def _redraw(self) -> None:
        ''' draws board: background, grid, jewels '''
        surface = pygame.display.get_surface()

        # background
        surface.fill(_BACKGROUND_COLOR)
        
        # grid
        self._draw_grid()
        
        # jewels
        self._draw_jewels()

        pygame.display.flip()

        self._game._delete_matches()

    def _draw_grid(self) -> None:
        ''' draws the grid (13x16) '''
        cols = self._game.get_cols()
        rows = self._game.get_rows()

        cell_width = self._surface_width // cols
        cell_height = self._surface_height // rows

        for row in range(rows):
            for col in range(cols):
                x = col * cell_width
                y = row * cell_height
                pygame.draw.rect(self._surface, (255, 255, 255), pygame.Rect(x , y, cell_width, cell_height), 1)

    def _draw_jewels(self) -> None:
        ''' draws the jewels '''
        rows = self._game.get_rows()
        cols = self._game.get_cols()

        for row in range(rows):
            for col in range(cols):
                jewel = self._state[row][col]
                if jewel != ' ':
                    self._draw_jewel(jewel, col, row)
    
    def _draw_jewel(self, jewel: str, col: int, row: int) -> None:
        ''' draws a specific jewel '''
        match_sound = pygame.mixer.Sound('ding.wav')

        color = get_color_from_value(int(''.join(filter(str.isdigit, jewel))))

        cell_width = self._surface_width // self._game.get_cols()
        cell_height = self._surface_height // self._game.get_rows()

        x = col * cell_width
        y = row * cell_height

        if 'AIR' in jewel:
            pygame.draw.ellipse(self._surface, color, (x, y, cell_width, cell_height))
        elif 'LANDED' in jewel or 'FROZEN' in jewel:
            pygame.draw.rect(self._surface, color, (x, y, cell_width, cell_height))
        elif 'MATCH' in jewel:
            pygame.draw.rect(self._surface, (255, 215, 0), (x, y, cell_width, cell_height))
            match_sound.play()

    def _end_game(self) -> None:
        ''' game ends '''
        self._running = False

    def _game_over_display(self) -> None:
        ''' game over display '''
        font = pygame.font.Font(None, 74)
        game_over_text = font.render("Game Over", True, (255, 0, 0))

        surface = pygame.display.get_surface()
        surface.fill(_BACKGROUND_COLOR)

        game_over_rect = game_over_text.get_rect(center=(self._surface_width // 2, self._surface_height // 3))
        surface.blit(game_over_text, game_over_rect)

        pygame.display.flip()

        pygame.time.wait(2000)

if __name__ == '__main__':
    ColumnsGame().run()