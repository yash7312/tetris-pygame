import pygame
import random
import copy #used in model to create buffer space to save the current state
pygame.font.init()


s_width = 800
s_height = 700
play_width = 300 
play_height = 600 
block_size = 30
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height



S = [['.....','.....','..00.','.00..','.....'],
     ['.....','..0..','..00.','...0.','.....']]

Z = [['.....','.....','.00..','..00.','.....'],
     ['.....','..0..','.00..','.0...','.....']]

I = [['..0..','..0..','..0..', '..0..','.....'],
     ['.....','0000.','.....','.....','.....']]

O = [['.....','.....','.00..','.00..','.....']]

J = [['.....','.0...','.000.','.....','.....'],
     ['.....','..00.','..0..','..0..','.....'],
     ['.....','.....','.000.','...0.','.....'],
     ['.....','..0..','..0..','.00..', '.....']]

L = [['.....','...0.','.000.','.....','.....'],
     ['.....','..0..','..0..','..00.','.....'],
     ['.....','.....','.000.','.0...', '.....'],
     ['.....','.00..','..0..','..0..', '.....']]

T = [['.....','..0..','.000.','.....','.....'],
     ['.....','..0..','..00.','..0..','.....'],
     ['.....','.....','.000.','..0..','.....'],
     ['.....','..0..','.00..','..0..','.....'],
     ]
P = [['.....','..0..','.000.','..0..','.....']]

shapes = [S, Z, I, O, J, L, T ,P]
shape_rotation = [(S, 2), (Z, 2), (I, 2), (O, 1), (J, 4), (L, 4), (T, 4), (P, 1)]
shape_colors = [(255, 60, 60), (255, 150, 60), (255, 255, 50), (160, 255, 128), (0, 180, 255), (166, 120, 255), (140, 220, 255) , (255,150,220)]
moves = [pygame.K_UP, pygame.K_RIGHT, pygame.K_LEFT]


class Piece(object):
    rows = 20  
    columns = 10  

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0  


def create_grid(locked_positions={}):
    grid = [[(255, 255, 255) for x in range(10)] for x in range(20)]  #rgb format color for each grid

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
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


def valid_space(shape, grid):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (255, 255, 255)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)

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

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), top_left_y + play_height / 2 - label.get_height() / 2))

 
def draw_main_menu(size,color,surface):
    font = pygame.font.SysFont('comicsans', size, bold=False)
    font_title = pygame.font.SysFont('comicsans', 2*size, bold=True)
    
    title = "T E T R I S"
    text1 = "Press Space To Play"
    text2 = "Press Esc to Quit"
    label1 = font.render(text1,1,color)
    label2 = font.render(text2,1,color)
    label_title = font_title.render(title,1,color)
    
    x1 = s_width / 2 - label1.get_width() / 2
    x2 = s_width / 2 - label2.get_width() / 2
    xt = s_width / 2 - label_title.get_width() / 2
    y1 = s_height /2 - label1.get_height() + label_title.get_height()
    y2 = s_height /2 - label2.get_height() + label1.get_height() + label_title.get_height()+ 10
    yt = s_height /2 - label_title.get_height()
    surface.blit(label_title, (xt,yt))
    
    surface.blit(label1, (x1,y1))
    surface.blit(label2, (x2, y2))

         
def draw_grid(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * 30),
                         (sx + play_width, sy + i * 30))  
        for j in range(col):
            pygame.draw.line(surface, (128, 128, 128), (sx + j * 30, sy),
                             (sx + j * 30, sy + play_height))
             

def clear_rows(grid, locked,score, cleared_lines):
    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        #Clear if there is no white pixels in the row
        if (255, 255, 255) not in row:
            inc += 1
            ind = i
            score[0] = score[0] + 10
            cleared_lines = cleared_lines + 1
            print(score)
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue               
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)


def draw_right_side(shape, surface,score):
    #Preview Next Shape
    font = pygame.font.SysFont('comicsans', 30)
    
    label = font.render('Next Shape', 1, (255, 255, 255))
    
    sx = top_left_x + play_width 
    sy = s_height / 2
    l  = (s_width - play_width) / 2
    x = sx + l/2 
    x_line = sx + l/2 -2.5*block_size
    format = shape.shape[shape.rotation % len(shape.shape)]
    
    for i, line in enumerate(format):
        row = list(line)  
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (x_line + j * block_size, sy + i * block_size, block_size, block_size), 0)
    for i in range(6):
        pygame.draw.line(surface, (64, 64, 64), (x_line, sy + i * block_size),
                         (x_line + 6*block_size, sy + i * block_size))
        for j in range(6):
            pygame.draw.line(surface, (64, 64, 64), (x_line + j * block_size, sy),
                             (x_line + j * block_size, sy + 6*block_size))
    surface.blit(label, (x- label.get_width()/2, sy - block_size))
    
    #Preview Score
    label1 = font.render("SCORE", 1, (255, 255, 255))
    label2 = font.render(score, 1, (255, 255, 255))
    
    surface.blit(label1, (x- label1.get_width()/2, sy + 5*block_size))
    surface.blit(label2, (x- label2.get_width()/2, sy + 6*block_size))


def draw_score(surface,score) :
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100
    font = pygame.font.SysFont('comicsans', 30)
    label1 = font.render("SCORE", 1, (255, 255, 255))
    label2 = font.render(str(score[0]), 1, (255, 255, 255))
    surface.blit(label1, (sx + 35, sy + 150))
    surface.blit(label2, (sx + 70, sy + 180))


def draw_window(surface):
    surface.fill((64, 64, 64))
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('T E T R I S', 1, (255, 255, 255))
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j * 30, top_left_y + i * 30, 30, 30), 0)      
    draw_grid(surface, 20, 10)
    pygame.draw.rect(surface, (100, 100, 100), (top_left_x, top_left_y, play_width, play_height), 5)



def getWeightedBlocks(locked_positions = {}): # return the change in this when move is Executed
    weightedSum = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                weightedSum += i*10
    locked_coords = locked_positions.keys()
    # print(locked_coords)
    
    save_weightedSum = weightedSum
    
    
    return weightedSum
                
    
def getRoughness(locked_positions = {}):
    abs_roughness = 0
    locked_coords = list(locked_positions.keys())
    filtered_coords = [(a, 20) for a in range(len(grid[0]))]

    for x, y in locked_coords:
        if y < filtered_coords[x][1]:
            filtered_coords[x] = (x, y)
    
    for i in range(len(filtered_coords)-1):
        abs_roughness += abs(filtered_coords[i][1] - filtered_coords[i+1][1])
    
    return abs_roughness

def getClearableLine(locked_positions={}):

    count = 0
    
    for i in range(len(grid)): # 0 is top
        for j in range(len(grid[i])):
            
            pass    
    
    return count



def main():
    genomes = []
    for s in range(10 ):
        genomes.append((random.uniform(-1,1),random.uniform(-1,1),random.uniform(-1,1),random.uniform(-1,1)))
    
    RankedGenomes = []
    
    for genome in genomes:
        RankedGenomes.append((run(genome), genome)) #score, genome_vars
    

def check_valid_move(move, current_piece):
    valid = 1
    if move == pygame.K_LEFT:
        current_piece.x -= 1
        if not valid_space(current_piece, grid):
            valid = 0
        current_piece.x += 1

    elif move == pygame.K_RIGHT:
        current_piece.x += 1
        if not valid_space(current_piece, grid):
            valid = 0
        current_piece.x -= 1
        
    elif move == pygame.K_UP:
        # rotate shape
        current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
        if not valid_space(current_piece, grid):
            valid = 0    
        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

    if move == pygame.K_DOWN:
        # move shape down
        current_piece.y += 1
        if not valid_space(current_piece, grid):
            valid = 0
        current_piece.y -= 1
        
    return  valid

all_possible_moves = []

def create_all_possible_moves():
    
    for i in range(4):
        temp = []
        for j in range(i+1):
            temp.append(pygame.K_RIGHT)
        for k in range(20-i-1):
            temp.append(pygame.K_DOWN)
        
        all_possible_moves.append(temp)
        
    for i in range(5):
        temp = []
        for j in range(i+1):
            temp.append(pygame.K_LEFT)
        for k in range(20-i-1):
            temp.append(pygame.K_DOWN)
        
        all_possible_moves.append(temp)
    
    print(len(all_possible_moves))

    

create_all_possible_moves()

def model(WeightedBlocks, Roughness, ClearableLine, LinesCleared, current_piece, grid, locked_positions, Score, cleared_lines):
    random.shuffle(moves)
    
    
    rough_score = 0
    # possible_moves = []
    possible_rotations = 0
    
    for x,y in shape_rotation:
        if(x == current_piece.shape):
            possible_rotations = y

    # execute all moves in order with one rotation at a time, 
    # its like a new piece only and compare the feature changes
    
    for rotation in range(possible_rotations):
        for possible_moves in all_possible_moves:
            rough_scores = []
            
            

    
    
    for move in moves:
        if(check_valid_move(move, current_piece) == 1):
            possible_moves.append(move)
    if(len(possible_moves) == 0):
        possible_moves = moves
            
    max = [0,random.choices(possible_moves, weights=[1 for i in range(len(possible_moves))], k=1)[0]]
    
    # check if move is possible or not, remove that move if not possible
    
    for move in possible_moves:
        # weights can be plus minus, chill
        
        # run the move, and compare initial and final states
        # make a buffer state with new locked positions, without the need for any display or colors
        # only locked positions are needed to know the state na
        
        
        buffer_grid = copy.deepcopy(grid)
        buffer_locked_positions = copy.deepcopy(locked_positions)
        buffer_Score = Score
        buffer_cleared_lines = cleared_lines

        game_over = False

        # Execute the move
        if move == pygame.K_LEFT:
            current_piece.x -= 1
            if not valid_space(current_piece, grid):
                current_piece.x += 1
        elif move == pygame.K_RIGHT:
            current_piece.x += 1
            if not valid_space(current_piece, grid):
                current_piece.x -= 1
        elif move == pygame.K_UP:
            current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)
            if not valid_space(current_piece, grid):
                current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape)
        elif move == pygame.K_DOWN:
            current_piece.y += 1
            if not valid_space(current_piece, grid):
                current_piece.y -= 1

        # Move down until locked
        # happening immediately, delay the timing
        clock = pygame.time.Clock()
        fall_time = 0

        while True:
            grid = create_grid(locked_positions)
            fall_speed = 0.05  # Adjust fall speed as needed

            fall_time += clock.get_rawtime()
            clock.tick()

            if fall_time / 100 >= fall_speed:
                fall_time = 0
                current_piece.y += 1
                if not valid_space(current_piece, grid) and current_piece.y > 0:
                    current_piece.y -= 1
                    
                    # Check for game over
                    if current_piece.y < 1:
                        game_over = True
                    break
            # Clear rows and update score
            clear_rows(grid, locked_positions, Score, cleared_lines)


        

        
        if check_lost(locked_positions):
            run = False
        
        # only 1 score, difference in respective features where needed
        if(game_over == False):
            
            
            u1 = getWeightedBlocks(buffer_locked_positions)
            u2 = getRoughness(buffer_locked_positions)
            u3 = getClearableLine(buffer_locked_positions)
            
            v1 = getWeightedBlocks(locked_positions)
            v2 = getRoughness(locked_positions)
            v3 = getClearableLine(locked_positions)
            
            abs1 = abs(v1 - u1)
            abs2 = abs(v2 - u2)
            abs3 = abs(v3 - u3)
            
            rough_score = abs1*WeightedBlocks + abs2*Roughness + abs3*ClearableLine + cleared_lines*LinesCleared
            
            if(rough_score > max[0]):
                max = [rough_score,move]
    
        # Restore the buffers
        grid = buffer_grid
        locked_positions = buffer_locked_positions
        Score = buffer_Score
        cleared_lines = buffer_cleared_lines
        

    
    key = max[1]
    # print(key)
    return key



def run(genome):
    global grid
    Score = [0]
    cleared_lines = 0
    locked_positions = {} #already placed blocks
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0

    while run:
        fall_speed = 0.05 # the lesser the faster it falls

        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick() # 1 ms

        if fall_time / 100 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        
        
        if(fall_time % 10 == 1):
            key = model(genome[0], genome[1], genome[2], genome[3], current_piece, grid, locked_positions, Score, cleared_lines) #CHANGE score[0] to number of lines cleared
            
            if key == pygame.K_LEFT:
                current_piece.x -= 1
                if not valid_space(current_piece, grid):
                    current_piece.x += 1

            elif key == pygame.K_RIGHT:
                current_piece.x += 1
                if not valid_space(current_piece, grid):
                    current_piece.x -= 1
            elif key == pygame.K_UP:
                # rotate shape
                current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                if not valid_space(current_piece, grid):
                    current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

            if key == pygame.K_DOWN:
                # move shape down
                current_piece.y += 1
                if not valid_space(current_piece, grid):
                    current_piece.y -= 1
        
        shape_pos = convert_shape_format(current_piece) 

   
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

      
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

    
            clear_rows(grid, locked_positions,Score,cleared_lines)

        draw_window(win)
        score = str(Score[0])
        draw_right_side(next_piece, win,score)
        pygame.display.update()
        
        
        

        if check_lost(locked_positions):
            run = False
            
    # draw_text_middle("You Lost : " + str(Score[0]), 40, (0, 0, 0), win)
    # pygame.display.update()
    # pygame.time.delay(2000)
    
    return Score[0]





def main_menu():
    clk = 0
    run = True
    color = (0,0,0)
    while run:
        if clk % 501 == 500 :
            color = random.choice(shape_colors)
        # win.fill(color)
        draw_main_menu(60,(255,255,255),win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE :
                    main()
                elif  event.key == pygame.K_ESCAPE :
                    run = False
        clk+=1            
    pygame.quit()




win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('T E T R I S')

main_menu()  

