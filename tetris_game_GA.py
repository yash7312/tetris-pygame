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
# right left down up
# 3 4 5 6
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

def getConnectedHoles(locked_positions={}):
    holes = 0
    for x in range(10):
        column_holes = 0
        block_found = False
        for y in range(20):
            if (x, y) in locked_positions:
                block_found = True
            elif block_found and (x, y) not in locked_positions:
                # Check if there is a block below the hole
                for k in range(y + 1, 20):
                    if (x, k) in locked_positions:
                        column_holes += 1
                        break
    holes += column_holes
    return holes

def getBlocks(locked_positions={}):
    blocks = 0
    for pos in locked_positions:
        if locked_positions[pos] != (255, 255, 255):  # Check if the position is not white (empty)
            blocks += 1
    return blocks

def getDeepestWell(locked_positions={}):
    deepest_well = 0
    for x in range(10):
        column_depth = 0
        for y in range(20):
            if (x, y) not in locked_positions:
                column_depth = y
            else:
                break
        deepest_well = max(deepest_well, column_depth)
    return deepest_well
    
def getColHoles(locked_positions={}):
    col_holes = 0
    for x in range(10):
        for y in range(20):
            if (x, y) in locked_positions:
                for z in range(y + 1, 20):
                    if (x, z) not in locked_positions:
                        col_holes += 1
                        y = 20
                        break
    return col_holes

def getPitHolePercent(locked_positions={}):
    pits = 0
    holes = 0
    for x in range(10):
        column_pits = 0
        column_holes = 0
        block_found = False
        for y in range(20):
            if (x, y) in locked_positions:
                block_found = True
            elif block_found and (x, y) not in locked_positions:
                column_holes += 1
            elif not block_found and (x, y) not in locked_positions:
                column_pits += 1
        pits += column_pits
        holes += column_holes
    if pits + holes == 0:
        return 0
    return pits / (pits + holes)


# use this to keep track if tetrise formed in current run, like number of cleared lines
def getTetrises(locked_positions={}):
    tetrises = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (255, 255, 255) not in row:
            if i >= 3:
                above_row = grid[i-1]
                above_above_row = grid[i-2]
                above_above_above_row = grid[i-3]
                if (255, 255, 255) not in above_row and (255, 255, 255) not in above_above_row and (255, 255, 255) not in above_above_above_row:
                    tetrises += 1
    return tetrises

modulo = 5
num_child = 0
num_gen = 0

def main():
    run((-0.007507249887295392, -0.10698963555753394, 0.25222830968334836, 0.32430588907638563, -0.007501497398399344, -0.10696146268886685, 0.2523695116026171, 0.3244348314506573, -0.007503637271966925, -0.10696089055761533))
    genomes = []
    for s in range(num_child):
        genomes.append((random.uniform(-1,0),  # WeightedBlocks 0
                        random.uniform(-1,0),  # Roughness      1
                        random.uniform(-1,1),  # ClearableLine  2
                        random.uniform( 0,1),  # LinesCleared   3
                        random.uniform(-1,1),  # ConnectedHoles 4
                        random.uniform(-1,1),  ## Blocks        5
                        random.uniform(-1,1),  # DeepestWell    6
                        random.uniform(-1,1),  # ColHoles       7
                        random.uniform(-1,1),  # PitHolePercent 8
                        random.uniform(-1,1))) # Tetrises       9
    
    for i in range(num_gen):
        print(f"GENERATION: {i}")
        RankedGenomes = []
        # print("KHTMMMMM")
        for genome in genomes:
            # print(len(genome))
            print(genome)
            RankedGenomes.append((run(genome), genome)) #score, genome_vars

        RankedGenomes.sort(reverse=True)
        
        # print(f"==== Gen  {i} {run((RankedGenomes[0][1][0],RankedGenomes[0][1][1],RankedGenomes[0][1][2]))} best solutions === ")
        # print(RankedGenomes[0])
        
        bestGenomes = RankedGenomes[:10]
        
        elements1 = []
        elements2 = []
        elements3 = []
        elements4 = []
        elements5 = []
        elements6 = []
        elements7 = []
        elements8 = []
        elements9 = []
        elements10 = []
        
        
        for s in bestGenomes:
            elements1.append(s[1][0])
            elements2.append(s[1][1])
            elements3.append(s[1][2])
            elements4.append(s[1][3])
            elements5.append(s[1][0])
            elements6.append(s[1][1])
            elements7.append(s[1][2])
            elements8.append(s[1][3])
            elements9.append(s[1][0])
            elements10.append(s[1][1])
            
            
        newGen = []
        for _ in range(num_child):
            e1 = random.choice(elements1) * random.uniform(0.999,1.001)
            e2 = random.choice(elements2) * random.uniform(0.999,1.001)
            e3 = random.choice(elements3) * random.uniform(0.999,1.001)
            e4 = random.choice(elements4) * random.uniform(0.999,1.001)
            e5 = random.choice(elements5) * random.uniform(0.999,1.001)
            e6 = random.choice(elements6) * random.uniform(0.999,1.001)
            e7 = random.choice(elements7) * random.uniform(0.999,1.001)
            e8 = random.choice(elements8) * random.uniform(0.999,1.001)
            e9 = random.choice(elements9) * random.uniform(0.999,1.001)
            e10 = random.choice(elements10) * random.uniform(0.999,1.001)
            
            
            newGen.append((e1,e2,e3,e4,e5,e6,e7,e8,e9,e10))
    
        genomes = newGen
    

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
    
    # print(len(all_possible_moves))

# print(moves)

create_all_possible_moves()
# for i in all_possible_moves:
#     print(i)
# print(all_possible_moves)
def model(tupple, current_piece, grid, locked_positions, Score, cleared_lines):
    WeightedBlocks = tupple[0]
    Roughness = tupple[1]
    ClearableLine = tupple[2]
    LinesCleared = tupple[3]
    ConnectedHoles = tupple[4]

    Blocks = tupple[5]
    DeepestWell = tupple[6]
    ColHoles = tupple[7]
    PitHolePercent = tupple[8]
    Tetrises = tupple[9]
    
    # random.shuffle(moves)
    rough_score = 0
    # possible_moves = []
    possible_rotations = 0
    
    clock = pygame.time.Clock()
    fall_time = 0
    
    # evaluate new pieces we can get after a rotation, like rotating doesn't do anything
    # to plus and square
    # print(current_piece.shape)
    # print()
    for x,y in shape_rotation:
        if(x == current_piece.shape):
            possible_rotations = y
            break

    # execute all moves in order with one rotation at a time, 
    # its like a new piece only and compare the feature changes
    for _ in range(possible_rotations):
        rough_scores = []
        
        for possible_moves in all_possible_moves:
            
            fall_time += clock.get_rawtime()
            clock.tick()
            # print("HIEEEEE")
            if(fall_time % 1 == 1):
                fall_time = 0
                
                buffer_grid = copy.deepcopy(grid)
                buffer_locked_positions = copy.deepcopy(locked_positions)
                buffer_Score = Score
                buffer_cleared_lines = cleared_lines
                buffer_piece = current_piece
                
                rough_score = 0
                # print("HIEEEEE")
                for move in possible_moves:
                    # print("HIEEEEE")
                    # weights can be plus minus, chill
                    
                    # run the move, and compare initial and final states
                    # make a buffer state with new locked positions, without the need for any display or colors
                    # only locked positions are needed to know the state na

                    game_over = False
                    change_piece = False
                    
                    
                    current_piece.y += 1
                    if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                        current_piece.y -= 1
                        change_piece = True
                    
                    # Execute the move
                    if move == pygame.K_LEFT:
                        current_piece.x -= 1
                        if not valid_space(current_piece, grid):
                            current_piece.x += 1
                    elif move == pygame.K_RIGHT:
                        current_piece.x += 1
                        if not valid_space(current_piece, grid):
                            current_piece.x -= 1
                    
                    elif move == pygame.K_DOWN:
                        current_piece.y += 1
                        if not valid_space(current_piece, grid):
                            current_piece.y -= 1

                    # Clear rows and update score
                    clear_rows(grid, locked_positions, Score, cleared_lines)

                    shape_pos = convert_shape_format(current_piece)

            
                    for i in range(len(shape_pos)):
                        x, y = shape_pos[i]
                        if y > -1:
                            grid[y][x] = current_piece.color

                
                    if change_piece:
                        for pos in shape_pos:
                            p = (pos[0], pos[1])
                            locked_positions[p] = current_piece.color
                        change_piece = False
                    
                    if check_lost(locked_positions):
                        game_over = True
                        break
                    
                # only 1 score, difference in respective features where needed
                if(game_over == False):
                    
                    try:
                        u1 = getWeightedBlocks(buffer_locked_positions)
                        u2 = getRoughness(buffer_locked_positions)
                        u3 = getClearableLine(buffer_locked_positions)
                        u4 = getConnectedHoles(buffer_locked_positions)
                        u5 = getBlocks(locked_positions)
                        u6 = getDeepestWell(locked_positions)
                        u7 = getColHoles(locked_positions)
                        u8 = getPitHolePercent(locked_positions)
                        # u9 is tetrises but similar treatement with cleared lines
                        
                        
                        v1 = getWeightedBlocks(locked_positions)
                        v2 = getRoughness(locked_positions)
                        v3 = getClearableLine(locked_positions)
                        v4 = getConnectedHoles(locked_positions)
                        v5 = getBlocks(locked_positions)
                        v6 = getDeepestWell(locked_positions)
                        v7 = getColHoles(locked_positions)
                        v8 = getPitHolePercent(locked_positions)
                        
                        abs1 = abs(v1 - u1)
                        abs2 = abs(v2 - u2)
                        abs3 = abs(v3 - u3)
                        abs4 = abs(v4 - u4)
                        abs5 = abs(v5 - u5)
                        abs6 = abs(v6 - u6)
                        abs7 = abs(v7 - u7)
                        abs8 = abs(v8 - u8)
                        
                        rough_score += abs1*WeightedBlocks 
                        rough_score += abs2*Roughness
                        rough_score += abs3*ClearableLine
                        rough_score += cleared_lines*LinesCleared
                        rough_score += abs4*ConnectedHoles
                        rough_score += abs5*Blocks
                        rough_score += abs6*DeepestWell
                        rough_score += abs7*ColHoles
                        rough_score += abs8*PitHolePercent
                    
                    except Exception as e:
                        print(f"Error calculating rough score: {e}")
                        rough_score = 0 
                        
                else:
                    rough_score = 0
                
                # Restore the buffers
                try:
                    grid = buffer_grid
                    locked_positions = buffer_locked_positions
                    Score = buffer_Score
                    cleared_lines = buffer_cleared_lines
                    current_piece = buffer_piece
                except Exception as e:
                    print(f"Error restoring buffers: {e}")
                
                try:
                    rough_scores.append(rough_score)
                except Exception as e:
                    print(f"Error appending rough score: {e}")

        
        # rotate
        try:
            possible_moves.pop()
            possible_moves.insert(0, pygame.K_UP)
        except Exception as e:
            print(f"Error rotating possible moves: {e}")
 
    # print("POTATO", (rough_scores))
    try:
        # consider rotation, len = possible_rotn * all_possible_moves
        max_index = rough_scores.index(max(rough_scores))
        # print(max(rough_score))
        rotated_amount = int(max_index / len(all_possible_moves))
        
        max_index %= len(all_possible_moves)
        
        key = all_possible_moves[max_index]
        
        for _ in range(rotated_amount):
            key.pop()
            key.insert(0, pygame.K_UP)
        
    except Exception as e:
        # print(f"Error selecting best moveeee: {e}")
        key = random.choice(all_possible_moves)
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
        # fall_speed = 0.05 # the lesser the faster it falls
        # print(clock.get_rawtime())
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick() # 1 ms

        if fall_time % modulo == 1:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        # if fall_time % 100 == 1:
        #     run = False

        running_moves = []
        
        tupple = [0] * len(genome)
        # print(len(genome))
        for i in range(len(genome)):
            tupple[i] = genome[i]
            
        running_moves = model(tupple, current_piece, grid, locked_positions, Score, cleared_lines) #CHANGE score[0] to number of lines cleared
        # running_moves = moves
        # print(running_moves[0])
        # print(pygame.K_LEFT)
        # key = pygame.K_DOWN
        # print(len(running_moves))
        
        
        #running throught moves, everything happens here
        for i in range(len(running_moves)):
            
            grid = create_grid(locked_positions)    
            fall_time += clock.get_rawtime()
            clock.tick() # 1 ms

            
            
            
                
            if fall_time % modulo == 2:
                fall_time = 0
                current_piece.y += 1
                if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                    current_piece.y -= 1
                    change_piece = True
            
            # print("HIIIIEEE")
            if(i >= 3):
                # change_piece = True
                break
                
            try:
                key = running_moves[i]
            except Exception as e:
                print(f"Error in key: {e} with i = {i}")
                break
            # print(i)
            # print(key)
            if(fall_time % modulo == 3):
                # key = model(genome[0], genome[1], genome[2], genome[3], current_piece, grid, locked_positions, Score, cleared_lines) #CHANGE score[0] to number of lines cleared
                
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
        # main()
        # run = False
        clk+=1            
    pygame.quit()




win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('T E T R I S')

main_menu()  

