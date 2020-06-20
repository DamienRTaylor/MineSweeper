import pygame
import random as r
import time
from math import floor, inf
class board:
    #                 (Width,Height)
    prevtime = 0.0
    def __init__(self,BoardSpots,numOfMines,DisplayRes,menuBuffer):
        self.MenuBuffer = menuBuffer
        self.tiles = [[0 for x in range(BoardSpots[0])] for y in range(BoardSpots[1])]
        self.Width = BoardSpots[0]
        self.Height = BoardSpots[1]
        self.numOfMines = numOfMines
        self.display = pygame.display.set_mode(DisplayRes)
        self.RemainingTiles = (self.Width * self.Height) -numOfMines
        for m in range(numOfMines):
            while True:
                x_mine = r.randint(0,self.Width-1)
                y_mine = r.randint(0,self.Height-1)
                if self.tiles[x_mine][y_mine] == 0:
                    self.tiles[x_mine][y_mine] = 1
                    break
        self.tiles = tile.convert_to_tile_list(self)

    def game_over_sequance(self):
        print("you lose")
        self.display.fill((0,0,0))

        for row in Board.tiles:
            for tile in row:
                tile.isRevealed = True
                tile.img = tile.get_self_image()
                self.display.blit(pygame.transform.scale(tile.img,(floor(self.display.get_size()[0]/self.Width),floor(self.display.get_size()[1]/self.Height))),(tile.pos[0][0],tile.pos[0][1]))
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

    def victory_sequance(self):
        print("you win")
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
    @staticmethod
    def calc_fps():
        now = time.time()
        try:
            fps = 1/(now-board.prevtime)
        except ZeroDivisionError:
            fps = inf #math module value that represents infinity, since the time between frames can't be determined, requesting the fps will just give inf

        board.prevtime = now
        return fps


class tile:
    def __init__(self,Board,x,y):
        self.isMine = bool(Board.tiles[x][y])
        self.x = x
        self.y = y
        self.isFlagged = False
        self.isRevealed = False
        self.surroundingMines = 0
        self.board = Board
        for posMod in [(0,1),(0,-1),(1,0),(-1,0)]:
            try:
                if x+posMod[0] >= 0 and y+posMod[1] >= 0:
                    if Board.tiles[x + posMod[0]][y + posMod[1]]:
                        self.surroundingMines+=1
            except IndexError:
                pass
        self.img = self.get_self_image()
                #   top left, top right , bottom Left, bottom right
        self.pos = self.get_pos_values()
    def set_flagged(self):
        self.isFlagged = not self.isFlagged
        self.img = self.get_self_image()
        self.board.display.blit(pygame.transform.scale(self.img,(floor(self.board.display.get_size()[0]/self.board.Width),floor(self.board.display.get_size()[1]/self.board.Height))),self.pos[0])
        pygame.display.update()

    def reveal(self):
        if not self.isRevealed:
            self.isRevealed = True
            self.img = self.get_self_image()
            self.board.display.blit(pygame.transform.scale(self.img,(floor(self.board.display.get_size()[0]/self.board.Width),floor(self.board.display.get_size()[1]/self.board.Height))),self.pos[0])
            pygame.display.update()
            if self.isMine:
                return False
            else:
                self.board.RemainingTiles-=1
                return True

    def get_self_image(self):
        img = ""
        if not self.isRevealed:
            if self.isFlagged:
                img = "Assets\\MINESWEEPER_F.png"
            else:
                img = "Assets\\MINESWEEPER_X.png"
        elif self.isMine:
            img = "Assets\\MINESWEEPER_M.png"
        else:
            img = "Assets\\MINESWEEPER_{}.png".format(str(self.surroundingMines))


        return pygame.image.load(img)

    def get_pos_values(self):

        topLeft = (self.x * floor(self.board.display.get_size()[0]/self.board.Width), self.y * floor(self.board.display.get_size()[1]/self.board.Height)+self.board.MenuBuffer)
        topRight = (topLeft[0] + floor(self.board.display.get_size()[0]/self.board.Width),topLeft[1])
        bottomLeft = (topLeft[0], topLeft[1] - floor(self.board.display.get_size()[1]/self.board.Height))
        bottomRight = (topRight[0],bottomLeft[1])
        return (topLeft,topRight,bottomLeft,bottomRight)

    @staticmethod
    def convert_to_tile_list(Board):
        tiles = []
        for x in range(Board.Width):
            tiles.append([])
            for y in range(Board.Height):
                tiles[x].append(tile(Board,x,y))
        return tiles



pygame.display.set_caption("MINESWEEPER")
pygame.display.set_icon(pygame.image.load("Assets\\MINESWEEPER_C.png"))
pygame.init()



active = True
Board = board((20,20),70,(960,980),20)
for row in Board.tiles:
    for tile in row:
        Board.display.blit(pygame.transform.scale(tile.img,(floor(Board.display.get_size()[0]/Board.Width),floor(Board.display.get_size()[1]/Board.Height))),(tile.pos[0][0],tile.pos[0][1]))
pygame.display.update()

while active:
    now = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # reveal block
                mouse_pos = pygame.mouse.get_pos()
                tile_x = floor(mouse_pos[0] / floor(Board.display.get_size()[0]/Board.Width))
                tile_y =floor((mouse_pos[1] - Board.MenuBuffer) /floor(Board.display.get_size()[1]/Board.Height))
                if Board.tiles[tile_x][tile_y].reveal() == False:
                    """returns false if a mine is hit,
                    would do if not board.func but if the square has been pressed before it returns None and not None == True, which would be a false you lose"""
                    Board.game_over_sequance()
                    active = False

                elif Board.RemainingTiles == 0: #checking if all the non mine tiles have been cleared
                        Board.victory_sequance()
                        active = False

            elif event.button == 3: #flagBlock
                mouse_pos = pygame.mouse.get_pos()
                tile_x = floor(mouse_pos[0] / floor(Board.display.get_size()[0]/Board.Width))
                tile_y =floor((mouse_pos[1] - Board.MenuBuffer) /floor(Board.display.get_size()[1]/Board.Height))
                Board.tiles[tile_x][tile_y].set_flagged()
