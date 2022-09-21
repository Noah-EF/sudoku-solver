# Noah Flanagan
# Python Sudoku Solving Application
# Idea from Lockheed Martin Codequest 2019 problems
import copy
import pygame
pygame.init()
#win = pygame.display.set_mode((700, 700), pygame.FULLSCREEN)
win = pygame.display.set_mode((700, 700))
pygame.display.set_caption("Sudoku Solver")
# this is currently unnecessary but was used for debugging
boardIn = [[0, 0, 0, 0, 0, 0, 0, 0, 3],
         [0, 0, 0, 0, 4, 0, 0, 8, 0],
         [3, 7, 1, 5, 0, 6, 0, 2, 0],
         [0, 0, 7, 4, 0, 0, 0, 1, 0],
         [4, 0, 0, 0, 7, 0, 0, 0, 9],
         [0, 6, 0, 0, 0, 8, 7, 0, 0],
         [0, 8, 0, 9, 0, 4, 5, 3, 7],
         [0, 9, 0, 0, 3, 0, 0, 0, 0],
         [2, 0, 0, 0, 0, 0, 0, 0, 0]]
# link to this puzzle https://www.websudoku.com/?level=3 #5,576,006,101
def getPresets(board):
    # returns a list of the coordinates of all given spots in the original puzzle
    # needed to ensure solution finder does not edit conditions
    presets = []
    for y in range(9):
        for x in range(9):
           if (board[y][x] != 0):
               presets.append([x, y])
    return presets

def next(loc):
    location = [loc[0], loc[1]]
    if (location[0]<8):
        location[0]+=1
    elif (location[0]==8):
        location[0] = 0
        location[1] += 1
    return location

def back(loc):
    location = [loc[0], loc[1]]
    if (location[0]>0):
        location[0]-=1
        #print('back x')
    else:
        if loc[0]==0:
            location[0] = 8
            location[1] -=1
            #print('back line')
    return location
def createSol(board):
    presets = getPresets(board)
    location = [0, 0]
    while (not valid_solution(board)):
        #print(location)
        #printBoard(board)
        if board[location[1]][location[0]] == 0:
            board[location[1]][location[0]] += 1
        elif location in presets:
            location = next(location)
        elif board[location[1]][location[0]] >9:
            board[location[1]][location[0]]=0
            location = back(location)
            while location in presets:
                location = back(location)
            board[location[1]][location[0]] += 1
        elif check_error(board):
            location = next(location)
            #print(location)
            #printBoard(board)
        elif board[location[1]][location[0]] >= 9:
            board[location[1]][location[0]] = 0
            location = back(location)
            while location in presets:
                location = back(location)
            board[location[1]][location[0]] += 1
        else:
            # this should be the case where the number at location is wrong and needs to go up to have that checked
            board[location[1]][location[0]] += 1
    return board
# different functions to check solution for errors in progress
# will check against duplicates were they should not be
# true output does not necessarily indicate the solution is valid just that it is not wrong yet
def check_error(board):
    # False indicates an error present

    # checks all rows for duplicate digits(except 0)
    for x in range(9):
        for y in range(1, 10):
            if (board[x].count(y)>1):
                #print('row', x, 'spot',y)
                return False
    # checks all columns
    # makes new list to check called column
    for y in range(9):
        column = []
        for x in range(1, 10):
            column.append(board[x - 1][y])
        for x in range(1, 10):
            if (column.count(x) > 1):
                # print('column', y, 'spot', x)
                return False

    # checks all sub-blocks
    for y in range (0, 9, 3):
        for x in range(0, 9, 3):
            group = []
            for a in range(3):
                for b in range(3):
                    group.append(board[y + a][x + b])
            for z in range (1, 10):
                if (group.count(z)>1):
                    #print('Block', y, x, 'num', z)
                    return False
    return True
# functions to check given solutions
# takes in a solve attempt and returns if the solution is valid
# these functions check that all necessary digits are present
def valid_solution(board):
    for x in range(9):
        if (check_row(x, board)==False):
            return False
        if (check_column(x, board)==False):
            return False
    for x in range(0, 9, 3):
        for y in range(0, 9, 3):
            if(check_block(x, y, board)==False):
                return False
    return True
def check_row(row, board):
    # takes in index of row to check for validity
    for x in range(9):
        # print(board[row].index(3))
        try: board[row].index(x+1)
        except: return False
    return True
# next two functions will first put all blocks in sections into list first then check that list
def check_column(col,board):
    column = []
    # makes new list to check called column
    for x in range(9):
        column.append(board[x][col])
    for x in range(9):
        try: column.index(x+1)
        except: return False
    return True
def check_block(x, y, board):
    # takes in coordinates of top left point of sub-group
    group = []
    for a in range(3):
        for b in range(3):
            group.append(board[y+a][x+b])
    for x in range(9):
        try: group.index(x+1)
        except: return False
    return True
# button class courtesy of Tech With Tim
class button():
    def __init__(self, color, x, y, width, height, num=0):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.num = num

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 1, self.y - 1, self.width + 2, self.height + 2), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.num != 0:
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(str(self.num), 1, (0, 0, 0))
            win.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False
'''START OF UI'''
run = True
buttons = []
for x in range(9):
    row = []
    for y in range(9):
        row.append(button((255, 255, 255), 82+62*y, 42+62*x, 58, 58))
    buttons.append(row)
solveButton = button((0, 255, 0), 180, 610, 158, 58, num = 'Solve')
clearButton = button((255, 0, 0), 370, 610, 158, 58, num = 'Clear')

while run:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for x in buttons:
                for y in x:
                    if y.isOver(pos):
                        if y.num<=9:
                            y.num += 1
                        if y.num>9:
                            y.num = 0
            if solveButton.isOver(pos):
                for x in range(9):
                    for y in range(9):
                        boardIn[x][y] = buttons[x][y].num
                boardIn = createSol(boardIn)
                for x in range(9):
                    for y in range(9):
                        buttons[x][y].num = boardIn[x][y]
            if clearButton.isOver(pos):
                for x in buttons:
                    for y in x:
                        y.num = 0
    win.fill((255, 255, 255))
    for x in buttons:
        for y in x:
            pos = pygame.mouse.get_pos()
            if y.isOver(pos):
                y.draw(win, (0, 255, 0))
            else:
                y.draw(win, (0, 0, 0))
    pygame.draw.line(win, (0, 0, 0), (266, 41), (266, 596), 4)
    pygame.draw.line(win, (0, 0, 0), (266+186, 41), (266+186, 596), 4)
    pygame.draw.line(win, (0, 0, 0), (81, 226), (636, 226), 4)
    pygame.draw.line(win, (0, 0, 0), (81, 226+186), (636, 226+186), 4)
    solveButton.draw(win, (0 ,0, 0))
    clearButton.draw(win, (0, 0, 0))
    pygame.display.update()
pygame.quit()


