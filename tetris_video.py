import pygame
import random
 
"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""
 
pygame.font.init()
 
# GLOBALS VARS
s_width = 900
s_height = 850
play_width = 400  # meaning 300 // 10 = 30 width per block
play_height = 800  # meaning 600 // 20 = 20 height per blo ck
block_size = 40
 
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height
 
 
# SHAPE FORMATS
 
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]
 
Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]
 
I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]
 
O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]
 
J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]
 
L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]
 
T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]
 
shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (167, 167, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape
 
 
class Piece(object):
    rows = 20  # y
    columns = 10  # x
 
    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0  # number from 0-3
 
class Figures():
    def create_grid(locked_positions = {}):
        grid = [[(0,0,0) for x in range(10)] for x in range(20)]
    
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if (j,i) in locked_positions:
                    c = locked_positions[(j,i)]
                    grid[i][j] = c
        return grid
    
    
    def convert_shape_format(shape):
        positions = []
        format = shape.shape[shape.rotation % len(shape.shape)]
    
        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    positions.append((shape.x + j, shape.y + i))
    
        for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)
    
        return positions
    
    
    def valid_space(shape, self):
        accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
        accepted_positions = [j for sub in accepted_positions for j in sub]
        formatted = Figures.convert_shape_format(shape)
    
        for pos in formatted:
            if pos not in accepted_positions:
                if pos[1] > -1:
                    return False
    
        return True
    
    
    def check_lost(positions):
        for pos in positions:
            x, y = pos
            if y < 1:
                return True
        return False
    
    
    def get_shape():
        global shapes, shape_colors
    
        return Piece(5, 0, random.choice(shapes))
    
    
    def draw_text_middle(text, size, color, surface):
        font = pygame.font.SysFont('comicsans', size, bold=True)
        label = font.render(text, 1, color)
    
        surface.blit(label, (top_left_x + play_width/2 - (label.get_width() / 2), top_left_y + play_height/2 - label.get_height()/2))
    
    
    def draw_grid(surface, row, col):
        sx = top_left_x
        sy = top_left_y
        for i in range(row):
            pygame.draw.line(surface, (128,128,128), (sx, sy+ i*block_size), (sx + play_width, sy + i * block_size))  # horizontal lines
            for j in range(col):
                pygame.draw.line(surface, (128,128,128), (sx + j * block_size, sy), (sx + j * block_size, sy + play_height))  # vertical lines
    
    
    def clear_rows(grid, locked):
        # need to see if row is clear the shift every other row above down one
        score = 0
        inc = 0 
        for i in range(len(grid)-1,-1,-1):
            row = grid[i]
            if (0, 0, 0) not in row:
                inc += 1
                # add positions to remove from locked
                ind = i
                for j in range(len(row)):
                    try:
                        del locked[(j, i)]
                    except:
                        continue
        if inc > 0:
            if inc == 1:
                score += 100
            elif inc ==2:
                score += 300
            elif inc == 3:
                score +=700
            elif inc == 4:
                score+=1500
            for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
                x, y = key
                if y < ind:
                    newKey = (x, y + inc)
                    locked[newKey] = locked.pop(key)
        return score
    
    
    def draw_next_shape(shape, surface):
        font = pygame.font.SysFont('comicsans', 30) 
        label_1 = font.render('Следующая', 1, (255,255,255))
        label_2 = font.render('фигура', 1, (255,255,255))
    
        sx = top_left_x + play_width + 30
        sy = top_left_y + play_height/2 - 100
        format = shape.shape[shape.rotation % len(shape.shape)]
    
        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy+60 + i*block_size, block_size, block_size), 0)
    
        surface.blit(label_1, (sx + 10, sy- block_size))
        surface.blit(label_2, (sx + 10, sy- block_size//4))
    
    def draw_score_time(score, surface, sx, sy):
        font = pygame.font.Font(pygame.font.match_font('comicsans'), 30)
        clock = pygame.time.Clock()
        ticks=pygame.time.get_ticks()
        millis=ticks%1000
        seconds=int(ticks/1000 % 60)
        minutes=int(ticks/60000 % 24)
        out='{minutes:02d}:{seconds:02d}:{millis}'.format(minutes=minutes, millis=millis, seconds=seconds)
        # pygame.display.flip()
        clock.tick(60)

        label_1 = font.render("Счёт:", 1, (255,255,255))
        label_2 = font.render(str(score), 1,(255,255,255))
        label_3 = font.render(str(out), 1,(255,255,255))


        surface.blit(label_1, (sx + 10, sy- block_size))
        surface.blit(label_2, (sx + 10, sy- block_size//4))
        surface.blit(label_3, (play_width + 300,100))
        
        
        
        # 
    def draw_window(surface):
        surface.fill((0,0,0))
    
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                pygame.draw.rect(surface, grid[i][j], (top_left_x + j* block_size, top_left_y + i * block_size, block_size, block_size), 0)
    
        # draw grid and border
        Figures.draw_grid(surface, 20, 10)
        pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)

class Tetris: 
    def __init__(self):
        self.win = pygame.display.set_mode((s_width, s_height)) 
        self.vy = 0.27
        self.fig = Figures
    def main(self):
        global grid
        score = 0
    
        locked_positions = {}  # (x,y):(255,0,0)
        grid = self.fig.create_grid(locked_positions)

        change_piece = False
        run = True
        current_piece = self.fig.get_shape()
        next_piece = self.fig.get_shape()
        clock = pygame.time.Clock()
        fall_time = 0

    
        while run:
    
            grid = self.fig.create_grid(locked_positions)
            fall_time += clock.get_rawtime()
            clock.tick()
    
            # PIECE FALLING CODE
            if fall_time/1000 >= self.vy:
                fall_time = 0
                current_piece.y += 1
                if not (self.fig.valid_space(current_piece, grid)) and current_piece.y > 0:
                    current_piece.y -= 1
                    change_piece = True
    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.display.quit()
                    quit()
    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        current_piece.x -= 1
                        if not self.fig.valid_space(current_piece, grid):
                            current_piece.x += 1
    
                    elif event.key == pygame.K_RIGHT:
                        current_piece.x += 1
                        if not self.fig.valid_space(current_piece, grid):
                            current_piece.x -= 1
                    elif event.key == pygame.K_UP:
                        # rotate shape
                        current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                        if not self.fig.valid_space(current_piece, grid):
                            current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)
    
                    if event.key == pygame.K_DOWN:
                        # move shape down
                        current_piece.y += 1
                        if not self.fig.valid_space(current_piece, grid):
                            current_piece.y -= 1
    
                    if event.key == pygame.K_SPACE:
                        while self.fig.valid_space(current_piece, grid):
                            current_piece.y += 1
                        current_piece.y -= 1
    
            shape_pos = self.fig.convert_shape_format(current_piece)
    
            # add piece to the grid for drawing
            for i in range(len(shape_pos)):
                x, y = shape_pos[i]
                if y > -1:
                    grid[y][x] = current_piece.color
    
            # IF PIECE HIT GROUND
            if change_piece:
                for pos in shape_pos:
                    p = (pos[0], pos[1])
                    locked_positions[p] = current_piece.color
                current_piece = next_piece
                next_piece = self.fig.get_shape()
                change_piece = False
    
                # call four times to check for multiple clear rows
                score += self.fig.clear_rows(grid, locked_positions)

            self.fig.draw_window(self.win)
            self.fig.draw_next_shape(next_piece, self.win)
            self.fig.draw_score_time(score, self.win,s_width//7, s_height//2)
            pygame.display.update()
    
            # Check if user lost
            if self.fig.check_lost(locked_positions):
                run = False
        self.win.fill((0,0,0))
        self.fig.draw_text_middle("Вы проиграли", 100, (255,0,0), self.win)
        self.fig.draw_score_time(score, self.win, s_width//2, s_height//2 + 150)
        pygame.display.update()
        pygame.time.wait(5000)
    
    
    def main_menu(self):
        self.fig = Figures
        run = True
        while run:
            self.win.fill((0,0,0))
            self.fig.draw_text_middle('Нажмите любую кнопку, чтобы начать', 40, (255, 255, 255), self.win)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
    
                if event.type == pygame.KEYDOWN:
                    Tetris.main(self)
        pygame.quit()
    
if __name__ == '__main__':
    pygame.init()
    Tetris().main_menu()
