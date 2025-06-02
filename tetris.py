import random
import pygame

"""
10 x 20 grid
play_height = 2 * play_width

tetriminos:
    0 - S - green
    1 - Z - red
    2 - I - cyan
    3 - O - yellow
    4 - J - blue
    5 - L - orange
    6 - T - purple
"""
pygame.init()
pygame.font.init()



col = 10
row = 20
s_width = 950
s_height = 750
play_width = 300
play_height = 600
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height - 50

filepath = './highscore.txt'
fontpath = './Baymax.otf'
fontpath_mario = './Scumbria.otf'



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

I = [['.....',
      '..0..',
      '..0..',
      '..0..',
      '..0..'],
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
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]





class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0



def create_grid(locked_pos={}):
    grid = [[(0, 0, 0) for x in range(col)] for y in range(row)]



    for y in range(row):
        for x in range(col):
            if (x, y) in locked_pos:
                color = locked_pos[
                    (x, y)]
                grid[y][x] = color

    return grid


def convert_shape_format(piece):
    positions = []
    shape_format = piece.shape[piece.rotation % len(piece.shape)]

    '''
    e.g.
       ['.....',
        '.....',
        '..00.',
        '.00..',
        '.....']
    '''
    for i, line in enumerate(shape_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((piece.x + j, piece.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions



def valid_space(piece, grid):

    accepted_pos = [[(x, y) for x in range(col) if grid[y][x] == (0, 0, 0)] for y in range(row)]

    accepted_pos = [x for item in accepted_pos for x in item]

    formatted_shape = convert_shape_format(piece)

    for pos in formatted_shape:
        if pos not in accepted_pos:
            if pos[1] >= 0:
                return False
    return True



def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False



def get_shape():
    return Piece(5, 0, random.choice(shapes))



def draw_text_middle(text, size, color, surface):
    font = pygame.font.Font(fontpath_mario, size)
    font.set_bold(False)
    font.set_italic(True)

    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width/2 - (label.get_width()/2), top_left_y + play_height/2 - (label.get_height()/2)))



def draw_grid(surface):
    r = g = b = 0
    grid_color = (r, g, b)

    for i in range(row):
        # draw grey horizontal lines
        pygame.draw.line(surface, grid_color, (top_left_x, top_left_y + i * block_size),
                         (top_left_x + play_width, top_left_y + i * block_size))
        for j in range(col):
            # draw grey vertical lines
            pygame.draw.line(surface, grid_color, (top_left_x + j * block_size, top_left_y),
                             (top_left_x + j * block_size, top_left_y + play_height))



def clear_rows(grid, locked):

    increment = 0
    for i in range(len(grid) - 1, -1, -1):
        grid_row = grid[i]
        if (0, 0, 0) not in grid_row:
            increment += 1

            index = i
            for j in range(len(grid_row)):
                try:
                    del locked[(j, i)]
                except ValueError:
                    continue


    if increment > 0:

        for key in sorted(list(locked), key=lambda a: a[1])[::-1]:
            x, y = key
            if y < index:
                new_key = (x, y + increment)
                locked[new_key] = locked.pop(key)

    return increment


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont(fontpath, 40)
    font.set_bold(True)
    label = font.render('СЛЕДУЮЩАЯ ', 1, (255,255,255))
    label1 = font.render('ФИГУРА:', 1, (255, 255, 255))
    start_x = 700
    start_y = 300

    block_size = 30
    next_width = 6 * block_size
    next_height = 6 * block_size

    # Фон
    pygame.draw.rect(surface, (0, 0, 0), (start_x - 10, start_y - 10, next_width, next_height))
    pygame.draw.rect(surface, (255, 255, 255), (start_x - 10, start_y - 10, next_width, next_height), 2)

    surface.blit(label, (start_x - 10, start_y - 85))
    surface.blit(label1, (start_x + 30, start_y - 55))
    format = shape.shape[shape.rotation]

    for i, line in enumerate(format):
        for j, column in enumerate(line):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (start_x + j * block_size, start_y + i * block_size, block_size, block_size), 0)
def draw_window(surface, grid, score=0, last_score=0):
    background=pygame.image.load("1.PNG").convert()
    background=pygame.transform.scale(background,(950,800))
    surface.blit(background,( 0, 0))

    pygame.font.init()
    font = pygame.font.Font(fontpath_mario, 65)
    font.set_bold(True)  # отдельно устанавливаем жирность
    label = font.render('TETRIS', 1, (255, 255, 255))  

    surface.blit(label, ((top_left_x + play_width / 2) - (label.get_width() / 2), 30))

    # current score
    font = pygame.font.Font(fontpath, 30)
    label = font.render('СЧЕТ   ' + str(score) , 1, (255, 255, 255))

    start_x = top_left_x + play_width + 50
    start_y = top_left_y + (play_height / 2 - 100)

    surface.blit(label, (730, 490))

    # last score
    label_hi = font.render('РЕКОРД   ' + str(last_score), 1, (255, 255, 255))

    start_x_hi = top_left_x - 240
    start_y_hi = top_left_y + 200

    surface.blit(label_hi, (start_x_hi + 20, start_y_hi + 200))

    for i in range(row):
        for j in range(col):
            pygame.draw.rect(surface, grid[i][j],
                             (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)

    draw_grid(surface)

    border_color = (255, 255, 255)
    pygame.draw.rect(surface, border_color, (top_left_x, top_left_y, play_width, play_height), 4)





def update_score(new_score):
    score = get_max_score()

    with open(filepath, 'w') as file:
        if new_score > score:
            file.write(str(new_score))
        else:
            file.write(str(score))


def get_max_score():
    with open(filepath, 'r') as file:
        lines = file.readlines()        # reads all the lines and puts in a list
        score = int(lines[0].strip())   # remove \n

    return score


def main(window):
    locked_positions = {}
    create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.35
    level_time = 0
    score = 0
    last_score = get_max_score()

    while run:
        grid = create_grid(locked_positions)

        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()

        clock.tick()

        if level_time/1000 > 5:
            level_time = 0
            if fall_speed > 0.15:
                fall_speed -= 0.005

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1

                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1

                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

                elif event.key == pygame.K_UP:
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

        piece_pos = convert_shape_format(current_piece)

        for i in range(len(piece_pos)):
            x, y = piece_pos[i]
            if y >= 0:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in piece_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10
            update_score(score)

            if last_score < score:
                last_score = score

        draw_window(window, grid, score, last_score)
        draw_next_shape(next_piece, window)
        pygame.display.update()

        if check_lost(locked_positions):
            run = False

    draw_text_middle('Вы проиграли!', 30, (255, 255, 255), window)
    pygame.display.update()
    pygame.time.delay(2000)  # wait for 2 seconds
    main_menu(window)
    return


def main_menu(window):
    run = True
    while run:
        background = pygame.image.load("2.PNG").convert()
        background = pygame.transform.scale(background, (950, 800))
        window.blit(background, (0, 0))



        pygame.draw.rect(window, (0, 0, 0), (30,365, 900, 80))
        pygame.draw.rect(window, (255, 255, 255), (30,365,  900, 80), 2)
        draw_text_middle('Нажмите на любую кнопку, чтобы начать', 40, (255, 255, 255), window)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                main(window)  # Запуск игры
                run = False  # Выход из цикла меню


if __name__ == '__main__':
    win = pygame.display.set_mode((s_width, s_height))
    pygame.display.set_caption('Tetris')

    main_menu(win)  # start game