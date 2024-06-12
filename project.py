# Imports
import pygame
import sys
import random
import os

# Game Window
SCREEN_HEIGHT = 650
SCREEN_WIDTH = 1250
FPS = 30

# special variables for sizing
sprite_multiplier = 4


# Loading/building Game
class Game:
    def __init__(self):
        pygame.init()
        self.buildsfx = pygame.mixer.Sound("sfx/build.wav")
        self.itemsfx = pygame.mixer.Sound("sfx/explosion.wav")
        self.music = pygame.mixer.Sound("sfx/the wilds theme.wav")
        self.buttonsfx = pygame.mixer.Sound("sfx/blipSelect.wav")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        pygame.display.set_caption("The Wilds")

        # Material variables
        self.WOOD = 0
        self.STONE = 0
        self.DIRECTION = 0
        self.houseList = []

        self.gameStateManager = GameStateManager('start')
        self.open_world = Open_world(self.screen, self.gameStateManager)
        self.start = Start(self.screen, self.gameStateManager)
        self.village = Village(self.screen, self.gameStateManager)
        self.win = Win(self.screen,self.gameStateManager)
        self.open_world_t = Open_world_top(self.screen,self.gameStateManager)
        self.open_world_l = Open_world_left(self.screen,self.gameStateManager)
        self.open_world_r = Open_world_right(self.screen,self.gameStateManager)

        self.states = {'start':self.start, 'open_world_down':self.open_world, 'village':self.village, 'open_world_top':self.open_world_t, 'end':self.win, 'open_world_left':self.open_world_l, 'open_world_right':self.open_world_r}
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_z]:
                self.gameStateManager.set_state('village')

            self.states[self.gameStateManager.get_state()].run()

            pygame.display.update()
            self.clock.tick(FPS)

# Object class, works as a parent for every object in the game
class Object:
    def __init__(self, screen, x, y, name):
        self.name = name
        self.display = screen
        self.x = x
        self.y = y
    def draw(self):
        self.display.blit(self.sprite,(self.x,self.y))
#Object subclasses, as in Player, Destructable, Enemy
class Player(Object):
    def __init__(self, screen, x, y, speed):
        self.filenames = ["graphics/player1_down_idle.png", "graphics/player1_up_idle.png", "graphics/player1_side_idle.png"]
        self.sprite = pygame.image.load(self.filenames[0])
        self.sprite = pygame.transform.scale(self.sprite, (self.sprite.get_width()*sprite_multiplier,self.sprite.get_height()*sprite_multiplier))

        self.gameStateManager = GameStateManager
        self.down = self.sprite
        self.up = pygame.image.load(self.filenames[1])
        self.up = pygame.transform.scale(self.up, (self.up.get_width() * sprite_multiplier, self.up.get_height() * sprite_multiplier))

        self.left = pygame.image.load(self.filenames[2])
        self.left = pygame.transform.scale(self.left, (self.left.get_width() * sprite_multiplier, self.left.get_height() * sprite_multiplier))

        self.right = pygame.image.load(self.filenames[2])
        self.right = pygame.transform.scale(self.right, (self.right.get_width() * sprite_multiplier, self.right.get_height() * sprite_multiplier))
        self.right = pygame.transform.flip(self.right, True, False)

        self.display = screen
        self.x = x
        self.y = y
        self.speed = speed

    def checkmove(self):
        pressedKeys = pygame.key.get_pressed()
        if pressedKeys[pygame.K_RIGHT] or pressedKeys[pygame.K_d]:
            self.x += self.speed
            self.sprite = self.right
        if pressedKeys[pygame.K_LEFT] or pressedKeys[pygame.K_a]:
            self.x -= self.speed
            self.sprite = self.left
        if pressedKeys[pygame.K_UP] or pressedKeys[pygame.K_w]:
            self.y -= self.speed
            self.sprite = self.up
        if pressedKeys[pygame.K_DOWN] or pressedKeys[pygame.K_s]:
            self.y += self.speed
            self.sprite = self.down

        if self.x <= 0:
            self.x=0
        elif self.y <= 0:
            self.y=0
        elif self.x >= SCREEN_WIDTH - self.sprite.get_width():
            self.x = SCREEN_WIDTH - self.sprite.get_width()
        elif self.y >= SCREEN_HEIGHT - self.sprite.get_height():
            self.y = SCREEN_HEIGHT - self.sprite.get_height()

        if (game.gameStateManager.currentState) == "village":
            if self.x <= 0:
                if pressedKeys[pygame.K_LEFT] or pressedKeys[pygame.K_a]:
                    game.DIRECTION = 1
                    game.gameStateManager.set_state('open_world_left')
            if self.x >= SCREEN_WIDTH - self.sprite.get_width():
                if pressedKeys[pygame.K_RIGHT] or pressedKeys[pygame.K_d]:
                    game.DIRECTION = 2
                    game.gameStateManager.set_state('open_world_right')
            if self.y <= 0:
                if pressedKeys[pygame.K_UP] or pressedKeys[pygame.K_w]:
                    game.DIRECTION = 3
                    game.gameStateManager.set_state('open_world_top')
            if self.y >= SCREEN_HEIGHT - self.sprite.get_height():
                if pressedKeys[pygame.K_DOWN] or pressedKeys[pygame.K_s]:
                    game.DIRECTION = 4
                    game.gameStateManager.set_state('open_world_down')

        if (game.gameStateManager.currentState) == "open_world_down" or (game.gameStateManager.currentState) == "open_world_top" or (game.gameStateManager.currentState) == "open_world_left" or (game.gameStateManager.currentState) == "open_world_right":
            if self.x <= 0 and game.DIRECTION == 2:
                if pressedKeys[pygame.K_LEFT] or pressedKeys[pygame.K_a]:
                    game.DIRECTION = 0
                    game.gameStateManager.set_state("village")
            elif self.x >= SCREEN_WIDTH - self.sprite.get_width() and game.DIRECTION == 1:
                if pressedKeys[pygame.K_RIGHT] or pressedKeys[pygame.K_d]:
                    game.DIRECTION = 0
                    game.gameStateManager.set_state("village")
            if self.y <= 0 and game.DIRECTION == 4:
                if pressedKeys[pygame.K_UP] or pressedKeys[pygame.K_w]:
                    game.DIRECTION = 0
                    game.gameStateManager.set_state("village")
            elif self.y >= SCREEN_HEIGHT - self.sprite.get_height() and game.DIRECTION == 3:
                if pressedKeys[pygame.K_DOWN] or pressedKeys[pygame.K_s]:
                    game.DIRECTION = 0
                    game.gameStateManager.set_state("village")

class Destructable(Object):
    def __init__(self, screen, x, y, sprite_filename, break_time):
        self.display = screen
        self.sprite = pygame.image.load(sprite_filename)
        self.sprite = pygame.transform.scale(self.sprite, (self.sprite.get_width() * sprite_multiplier, self.sprite.get_height() * sprite_multiplier))
        self.x = x
        self.y = y
        self.break_time = break_time
        self.player_stop = False
        self.hitbox = pygame.Rect(self.x,self.y,self.sprite.get_width(),self.sprite.get_height())

class Buildable(Object):
    def __init__(self, screen, x, y, sprite_filename, wood_cost, stone_cost):
        self.display = screen
        self.sprite = pygame.image.load(sprite_filename)
        self.sprite = pygame.transform.scale(self.sprite, (self.sprite.get_width() * sprite_multiplier, self.sprite.get_height() * sprite_multiplier))
        self.x = x
        self.y = y
        self.wood_cost = wood_cost
        self.stone_cost = stone_cost
    def draw(self):
        self.display.blit(self.sprite,(self.x+self.sprite.get_width()/3,self.y-self.sprite.get_height()/3))

class BuildPlot(Object):
    def __init__(self,screen,x,y):
        self.display = screen
        self.sprite = pygame.image.load("graphics/buildplot.png")
        self.sprite = pygame.transform.scale(self.sprite, (self.sprite.get_width() * sprite_multiplier, self.sprite.get_height() * sprite_multiplier))
        self.x = x
        self.y = y
        self.hitbox = pygame.Rect(self.x,self.y,self.sprite.get_width(),self.sprite.get_height())
    def draw(self):
        self.display.blit(self.sprite,(self.x,self.y))

#Open world gameplay, breaking wood and stone
class Open_world:
    def __init__(self, display, gameStateManager):

        self.font1 = pygame.font.SysFont("comicsansms", 28)
        self.display = display
        self.gameStateManager = gameStateManager
        self.player = Player(self.display, self.display.get_width()/2, 108, 10)
        first_rock = Destructable(self.display, random.randint(136, self.display.get_width()-136), random.randint(108,self.display.get_height()-108), "graphics/rock.png", 5)
        first_tree = Destructable(self.display, random.randint(0, self.display.get_width()), random.randint(0,self.display.get_height()), "graphics/tree.png", 2)
        self.treeList = []
        self.treeList.append(first_tree)
        self.rockList = []
        self.rockList.append(first_rock)

        new_tree_x = random.randint((58 * sprite_multiplier), self.display.get_width() - (58 * sprite_multiplier))
        new_tree_y = random.randint((88), self.display.get_height() - (88))
        for i in range(random.randint(6, 9)):
            for trees in self.treeList:
                hitbox = pygame.Rect(trees.x, trees.y, trees.sprite.get_width(), trees.sprite.get_height())
                while hitbox.collidepoint(new_tree_x, new_tree_y):
                    new_tree_x = random.randint(trees.sprite.get_width(),
                                                self.display.get_width() - trees.sprite.get_width())
                    new_tree_y = random.randint(trees.sprite.get_height(),
                                                self.display.get_height() - trees.sprite.get_height())
            new_tree = Destructable(self.display, new_tree_x, new_tree_y, "graphics/tree.png", 5)
            self.treeList.append(new_tree)

        new_rock_x = random.randint(136, self.display.get_width() - (136))
        new_rock_y = random.randint((27 * sprite_multiplier), self.display.get_height() - (27 * sprite_multiplier))
        for i in range(random.randint(4, 6)):
            for rocks in self.rockList:
                hitbox = pygame.Rect(rocks.x, rocks.y, rocks.sprite.get_width(), rocks.sprite.get_height())
                while hitbox.collidepoint(new_rock_x, new_rock_y):
                    new_rock_x = random.randint(rocks.sprite.get_width(),
                                                self.display.get_width() - rocks.sprite.get_width())
                    new_rock_y = random.randint(rocks.sprite.get_height(),
                                                self.display.get_height() - rocks.sprite.get_height())
            new_rock = Destructable(self.display, new_rock_x, new_rock_y, "graphics/rock.png", 5)
            self.rockList.append(new_rock)

        global font
        font = pygame.font.SysFont("helveticams", 28)

        self.item_display = pygame.image.load('graphics/item_icon.png')
        self.item_display = pygame.transform.scale(self.item_display, (self.item_display.get_width()*2, self.item_display.get_height()*2))
        self.bg = pygame.image.load("graphics/forestbgdown.png")
        self.bg = pygame.transform.scale(self.bg, ((self.bg.get_width() * sprite_multiplier), (self.bg.get_height() * sprite_multiplier)))
        self.click_protect = True


    def run(self):
        self.display.blit(self.bg, (0, 0))

        self.player.draw()
        #please commit
        for rock in self.rockList:
            rock.draw()
        for tree in self.treeList:
            tree.draw()

        if not pygame.mouse.get_pressed()[0]:
            self.click_protect = True

        if pygame.mouse.get_pressed()[0]:
            self.click_protect = False
            for tree in self.treeList:
                if tree.hitbox.collidepoint(pygame.mouse.get_pos()):
                    self.treeList.remove(tree)
                    game.itemsfx.play()
                    game.WOOD += 1
            for rock in self.rockList:
                if rock.hitbox.collidepoint(pygame.mouse.get_pos()):
                    self.rockList.remove(rock)
                    game.itemsfx.play()
                    game.STONE += 1
        self.display.blit(self.item_display, (20,20))
        self.stone_score = font.render(str(game.STONE), True, (255,255,255))
        self.wood_score = font.render(str(game.WOOD), True, (255,255,255))
        self.display.blit(self.wood_score, (85, 40))
        self.display.blit(self.stone_score, (190, 40))
        self.player.checkmove()





#Open World Top
class Open_world_top:
    def __init__(self, display, gameStateManager):

        self.font1 = pygame.font.SysFont("comicsansms", 28)
        self.display = display
        self.gameStateManager = gameStateManager
        self.player = Player(self.display, self.display.get_width()/2, self.display.get_height()-108, 10)
        first_rock = Destructable(self.display, random.randint(136, self.display.get_width()-136), random.randint(108,self.display.get_height()-108), "graphics/rock.png", 5)
        first_tree = Destructable(self.display, random.randint(0, self.display.get_width()), random.randint(0,self.display.get_height()), "graphics/tree.png", 2)
        self.treeList = []
        self.treeList.append(first_tree)
        self.rockList = []
        self.rockList.append(first_rock)

        new_tree_x = random.randint((58 * sprite_multiplier), self.display.get_width() - (58 * sprite_multiplier))
        new_tree_y = random.randint((88), self.display.get_height() - (88))
        for i in range(random.randint(6, 9)):
            for trees in self.treeList:
                hitbox = pygame.Rect(trees.x, trees.y, trees.sprite.get_width(), trees.sprite.get_height())
                while hitbox.collidepoint(new_tree_x, new_tree_y):
                    new_tree_x = random.randint(trees.sprite.get_width(),
                                                self.display.get_width() - trees.sprite.get_width())
                    new_tree_y = random.randint(trees.sprite.get_height(),
                                                self.display.get_height() - trees.sprite.get_height())
            new_tree = Destructable(self.display, new_tree_x, new_tree_y, "graphics/tree.png", 5)
            self.treeList.append(new_tree)

        new_rock_x = random.randint(136, self.display.get_width() - (136))
        new_rock_y = random.randint((27 * sprite_multiplier), self.display.get_height() - (27 * sprite_multiplier))
        for i in range(random.randint(4, 6)):
            for rocks in self.rockList:
                hitbox = pygame.Rect(rocks.x, rocks.y, rocks.sprite.get_width(), rocks.sprite.get_height())
                while hitbox.collidepoint(new_rock_x, new_rock_y):
                    new_rock_x = random.randint(rocks.sprite.get_width(),
                                                self.display.get_width() - rocks.sprite.get_width())
                    new_rock_y = random.randint(rocks.sprite.get_height(),
                                                self.display.get_height() - rocks.sprite.get_height())
            new_rock = Destructable(self.display, new_rock_x, new_rock_y, "graphics/rock.png", 5)
            self.rockList.append(new_rock)

        global font
        font = pygame.font.SysFont("helveticams", 28)

        self.item_display = pygame.image.load('graphics/item_icon.png')
        self.item_display = pygame.transform.scale(self.item_display, (self.item_display.get_width()*2, self.item_display.get_height()*2))
        self.bg = pygame.image.load("graphics/forestbgtop.png")
        self.bg = pygame.transform.scale(self.bg, ((self.bg.get_width() * sprite_multiplier), (self.bg.get_height() * sprite_multiplier)))
        self.click_protect = True


    def run(self):
        self.display.blit(self.bg, (0, 0))

        self.player.draw()
        #please commit
        for rock in self.rockList:
            rock.draw()
        for tree in self.treeList:
            tree.draw()

        if not pygame.mouse.get_pressed()[0]:
            self.click_protect = True

        if pygame.mouse.get_pressed()[0]:
            self.click_protect = False
            for tree in self.treeList:
                if tree.hitbox.collidepoint(pygame.mouse.get_pos()):
                    self.treeList.remove(tree)
                    game.itemsfx.play()
                    game.WOOD += 1
            for rock in self.rockList:
                if rock.hitbox.collidepoint(pygame.mouse.get_pos()):
                    self.rockList.remove(rock)
                    game.itemsfx.play()
                    game.STONE += 1
        self.display.blit(self.item_display, (20,20))
        self.stone_score = font.render(str(game.STONE), True, (255,255,255))
        self.wood_score = font.render(str(game.WOOD), True, (255,255,255))
        self.display.blit(self.wood_score, (85, 40))
        self.display.blit(self.stone_score, (190, 40))
        self.player.checkmove()




#Open World Right
class Open_world_right:
    def __init__(self, display, gameStateManager):

        self.font1 = pygame.font.SysFont("comicsansms", 28)
        self.display = display
        self.gameStateManager = gameStateManager
        self.player = Player(self.display, 64, self.display.get_height()/2, 10)
        first_rock = Destructable(self.display, random.randint(136, self.display.get_width()-136), random.randint(108,self.display.get_height()-108), "graphics/rock.png", 5)
        first_tree = Destructable(self.display, random.randint(0, self.display.get_width()), random.randint(0,self.display.get_height()), "graphics/tree.png", 2)
        self.treeList = []
        self.treeList.append(first_tree)
        self.rockList = []
        self.rockList.append(first_rock)

        new_tree_x = random.randint((58 * sprite_multiplier), self.display.get_width() - (58 * sprite_multiplier))
        new_tree_y = random.randint((88), self.display.get_height() - (88))
        for i in range(random.randint(6, 9)):
            for trees in self.treeList:
                hitbox = pygame.Rect(trees.x, trees.y, trees.sprite.get_width(), trees.sprite.get_height())
                while hitbox.collidepoint(new_tree_x, new_tree_y):
                    new_tree_x = random.randint(trees.sprite.get_width(),
                                                self.display.get_width() - trees.sprite.get_width())
                    new_tree_y = random.randint(trees.sprite.get_height(),
                                                self.display.get_height() - trees.sprite.get_height())
            new_tree = Destructable(self.display, new_tree_x, new_tree_y, "graphics/tree.png", 5)
            self.treeList.append(new_tree)

        new_rock_x = random.randint(136, self.display.get_width() - (136))
        new_rock_y = random.randint((27 * sprite_multiplier), self.display.get_height() - (27 * sprite_multiplier))
        for i in range(random.randint(4, 6)):
            for rocks in self.rockList:
                hitbox = pygame.Rect(rocks.x, rocks.y, rocks.sprite.get_width(), rocks.sprite.get_height())
                while hitbox.collidepoint(new_rock_x, new_rock_y):
                    new_rock_x = random.randint(rocks.sprite.get_width(),
                                                self.display.get_width() - rocks.sprite.get_width())
                    new_rock_y = random.randint(rocks.sprite.get_height(),
                                                self.display.get_height() - rocks.sprite.get_height())
            new_rock = Destructable(self.display, new_rock_x, new_rock_y, "graphics/rock.png", 5)
            self.rockList.append(new_rock)

        global font
        font = pygame.font.SysFont("helveticams", 28)

        self.item_display = pygame.image.load('graphics/item_icon.png')
        self.item_display = pygame.transform.scale(self.item_display, (self.item_display.get_width()*2, self.item_display.get_height()*2))
        self.bg = pygame.image.load("graphics/forestbgleft.png")
        self.bg = pygame.transform.scale(self.bg, ((self.bg.get_width() * sprite_multiplier), (self.bg.get_height() * sprite_multiplier)))
        self.click_protect = True

    def run(self):
        self.display.blit(self.bg, (0, 0))

        self.player.draw()
        #please commit
        for rock in self.rockList:
            rock.draw()
        for tree in self.treeList:
            tree.draw()

        if not pygame.mouse.get_pressed()[0]:
            self.click_protect = True

        if pygame.mouse.get_pressed()[0]:
            self.click_protect = False
            for tree in self.treeList:
                if tree.hitbox.collidepoint(pygame.mouse.get_pos()):
                    self.treeList.remove(tree)
                    game.itemsfx.play()
                    game.WOOD += 1
            for rock in self.rockList:
                if rock.hitbox.collidepoint(pygame.mouse.get_pos()):
                    self.rockList.remove(rock)
                    game.itemsfx.play()
                    game.STONE += 1
        self.display.blit(self.item_display, (20,20))
        self.stone_score = font.render(str(game.STONE), True, (255,255,255))
        self.wood_score = font.render(str(game.WOOD), True, (255,255,255))
        self.display.blit(self.wood_score, (85, 40))
        self.display.blit(self.stone_score, (190, 40))
        self.player.checkmove()



#Open World Left
class Open_world_left:
    def __init__(self, display, gameStateManager):

        self.font1 = pygame.font.SysFont("comicsansms", 28)
        self.display = display
        self.gameStateManager = gameStateManager
        self.player = Player(self.display, self.display.get_width()-64, self.display.get_height()/2, 10)
        first_rock = Destructable(self.display, random.randint(136, self.display.get_width()-136), random.randint(108,self.display.get_height()-108), "graphics/rock.png", 5)
        first_tree = Destructable(self.display, random.randint(0, self.display.get_width()), random.randint(0,self.display.get_height()), "graphics/tree.png", 2)
        self.treeList = []
        self.treeList.append(first_tree)
        self.rockList = []
        self.rockList.append(first_rock)

        new_tree_x = random.randint((58*sprite_multiplier), self.display.get_width() - (58*sprite_multiplier))
        new_tree_y = random.randint((88), self.display.get_height() - (88))
        for i in range(random.randint(6, 9)):
            for trees in self.treeList:
                hitbox = pygame.Rect(trees.x, trees.y, trees.sprite.get_width(), trees.sprite.get_height())
                while hitbox.colliderect(pygame.Rect(new_tree_x, new_tree_y,trees.sprite.get_width(),trees.sprite.get_height())):
                    new_tree_x = random.randint(trees.sprite.get_width(),self.display.get_width() - trees.sprite.get_width())
                    new_tree_y = random.randint(trees.sprite.get_height(),self.display.get_height() - trees.sprite.get_height())
            new_tree = Destructable(self.display, new_tree_x, new_tree_y, "graphics/tree.png", 5)
            self.treeList.append(new_tree)


        new_rock_x = random.randint(136,self.display.get_width() - (136))
        new_rock_y = random.randint((27*sprite_multiplier),self.display.get_height() - (27*sprite_multiplier))
        for i in range(random.randint(4, 6)):
            for rocks in self.rockList:
                hitbox = pygame.Rect(rocks.x, rocks.y, rocks.sprite.get_width(), rocks.sprite.get_height())
                while hitbox.colliderect(pygame.Rect(new_rock_x, new_rock_y,rocks.sprite.get_width(),rocks.sprite.get_height())):
                    new_rock_x = random.randint(rocks.sprite.get_width(),self.display.get_width() - rocks.sprite.get_width())
                    new_rock_y = random.randint(rocks.sprite.get_height(),self.display.get_height() - rocks.sprite.get_height())
            new_rock = Destructable(self.display, new_rock_x, new_rock_y, "graphics/rock.png", 5)
            self.rockList.append(new_rock)

        global font
        font = pygame.font.SysFont("helveticams", 28)

        self.item_display = pygame.image.load('graphics/item_icon.png')
        self.item_display = pygame.transform.scale(self.item_display, (self.item_display.get_width()*2, self.item_display.get_height()*2))
        self.bg = pygame.image.load("graphics/forestbgright.png")
        self.bg = pygame.transform.scale(self.bg, ((self.bg.get_width() * sprite_multiplier), (self.bg.get_height() * sprite_multiplier)))
        self.click_protect = True

    def run(self):
        self.display.blit(self.bg, (0, 0))

        self.player.draw()
        #please commit
        for rock in self.rockList:
            rock.draw()
        for tree in self.treeList:
            tree.draw()

        if not pygame.mouse.get_pressed()[0]:
            self.click_protect = True

        if pygame.mouse.get_pressed()[0]:
            self.click_protect = False
            for tree in self.treeList:
                if tree.hitbox.collidepoint(pygame.mouse.get_pos()):
                    self.treeList.remove(tree)
                    game.itemsfx.play()
                    game.WOOD += 1
            for rock in self.rockList:
                if rock.hitbox.collidepoint(pygame.mouse.get_pos()):
                    self.rockList.remove(rock)
                    game.itemsfx.play()
                    game.STONE += 1
        self.display.blit(self.item_display, (20,20))
        self.stone_score = font.render(str(game.STONE), True, (255,255,255))
        self.wood_score = font.render(str(game.WOOD), True, (255,255,255))
        self.display.blit(self.wood_score, (85, 40))
        self.display.blit(self.stone_score, (190, 40))
        self.player.checkmove()



#Village gameplay, building haus
class Village:
    def __init__(self, display, gameStateManager):
        self.item_display = pygame.image.load('graphics/item_icon.png')
        self.item_display = pygame.transform.scale(self.item_display, (self.item_display.get_width() * 2, self.item_display.get_height() * 2))
        self.plotList = []
        self.font1 = pygame.font.SysFont("comicsansms", 28)
        self.display = display
        self.gameStateManager = gameStateManager
        self.buildplot1 = BuildPlot(self.display, 40, 130)
        self.buildplot2 = BuildPlot(self.display, 740, 130)
        self.buildplot3 = BuildPlot(self.display, 40, 500)
        self.buildplot4 = BuildPlot(self.display, 740, 500)
        self.plotList.append(self.buildplot1)
        self.plotList.append(self.buildplot2)
        self.plotList.append(self.buildplot3)
        self.plotList.append(self.buildplot4)
        self.player = Player(self.display, self.display.get_width()/2, self.display.get_height()/2, 10)

        global font
        font = pygame.font.SysFont("helveticams", 28)

        self.item_display = pygame.image.load('graphics/item_icon.png')
        self.item_display = pygame.transform.scale(self.item_display, (
        self.item_display.get_width() * 2, self.item_display.get_height() * 2))
        self.bg = pygame.image.load("graphics/villagebg.png")
        self.bg = pygame.transform.scale(self.bg, ((self.bg.get_width() * sprite_multiplier), (self.bg.get_height() * sprite_multiplier)))
        self.click_protect = True
        self.tutorial_text_trigger = True
        self.tutorial_text = font.render("Use 5 Logs and 4 Stone to Make a House!", True, (0,0,0))



    def run(self):
        self.display.blit(self.bg, (0, 0))
        for plot in self.plotList:
            plot.draw()
        self.player.draw()
        self.player.draw()

        if len(game.houseList) != 0:
            for house in game.houseList:
                house.draw()

        if len(game.houseList) == 1:
            self.tutorial_text_trigger = False

        if len(game.houseList) == 4:
            game.gameStateManager.set_state("end")

        self.display.blit(self.item_display, (20, 20))
        self.stone_score = font.render(str(game.STONE), True, (255, 255, 255))
        self.wood_score = font.render(str(game.WOOD), True, (255, 255, 255))
        self.display.blit(self.wood_score, (85, 40))
        self.display.blit(self.stone_score, (190, 40))
        if self.tutorial_text_trigger:
            self.display.blit(self.tutorial_text,(self.display.get_width()/3,40))

        self.player.checkmove()

        if not pygame.mouse.get_pressed()[0]:
            self.click_protect = True

        if pygame.mouse.get_pressed()[0] and self.click_protect:
            self.click_protect = False
            for plots in self.plotList:
                if plots.hitbox.collidepoint(pygame.mouse.get_pos()) and game.WOOD >= 5 and game.STONE >= 4:
                    new_house = Buildable(self.display, plots.x, plots.y-76, "graphics/house_mid.png", 5, 4)
                    game.buildsfx.play()
                    game.houseList.append(new_house)
                    self.plotList.remove(plots)
                    game.WOOD -= 5
                    game.STONE -= 4







#Start Screen/character chooser
class Start:
    def __init__(self, screen,gameStateManager):
        self.display = screen
        self.gameStateManager = gameStateManager
        self.play_button = pygame.image.load('graphics/button.png')
        self.play_button_down = pygame.image.load('graphics/buttonhover.png')
        self.bg = pygame.image.load("graphics/titlebg.png")

        self.play_button = pygame.transform.scale(self.play_button, (self.play_button.get_width() * sprite_multiplier, self.play_button.get_height() * sprite_multiplier))
        self.play_button_down = pygame.transform.scale(self.play_button_down, (self.play_button_down.get_width() * sprite_multiplier, self.play_button_down.get_height() * sprite_multiplier))
        self.bg = pygame.transform.scale(self.bg, (self.bg.get_width()*sprite_multiplier,self.bg.get_height()*sprite_multiplier))
        self.current_image = self.play_button

    def run(self):
        self.display.blit(self.bg,(0,0))
        button_rect = pygame.Rect(84, SCREEN_HEIGHT/2 - self.current_image.get_height()/2, self.current_image.get_width(), self.current_image.get_height())
        if pygame.mouse.get_pressed()[0] and button_rect.collidepoint(pygame.mouse.get_pos()):
            self.gameStateManager.set_state('village')
            game.buttonsfx.play()
            game.music.play(-1)
        if button_rect.collidepoint(pygame.mouse.get_pos()):
            self.current_image = self.play_button_down
        else:
            self.current_image = self.play_button
        self.display.blit(self.current_image, (84, SCREEN_HEIGHT/2 - self.current_image.get_height()/2))

#Win Screen
class Win:
    def __init__(self, screen,gameStateManager):
        self.display = screen
        self.gameStateManager = gameStateManager
        self.play_button = pygame.image.load('graphics/exitbutton.png')
        self.play_button_down = pygame.image.load('graphics/exitbutton_down.png')
        self.bg = pygame.image.load("graphics/end.png")
        self.bg = pygame.transform.scale(self.bg, (self.bg.get_width()*sprite_multiplier,self.bg.get_height()*sprite_multiplier))

        self.play_button = pygame.transform.scale(self.play_button, (self.play_button.get_width() * sprite_multiplier, self.play_button.get_height() * sprite_multiplier))
        self.play_button_down = pygame.transform.scale(self.play_button_down, (self.play_button_down.get_width() * sprite_multiplier, self.play_button_down.get_height() * sprite_multiplier))

        self.current_image = self.play_button
        self.click_protection = False


    def run(self):
        self.display.blit(self.bg,(0,0))
        button_rect = pygame.Rect(84, SCREEN_HEIGHT/2 - self.current_image.get_height()/2, self.current_image.get_width(), self.current_image.get_height())
        if pygame.mouse.get_pressed()[0] and button_rect.collidepoint(pygame.mouse.get_pos()) and not self.click_protection:
            game.buttonsfx.play()
            self.click_protection = True
            sys.exit()

        if button_rect.collidepoint(pygame.mouse.get_pos()):
            self.current_image = self.play_button_down
        else:
            self.current_image = self.play_button

        self.display.blit(self.current_image, (84, SCREEN_HEIGHT/2 - self.current_image.get_height()/2))


#Game state manager for scenes
class GameStateManager:
    def __init__(self,currentState):
        self.currentState = currentState
    def get_state(self):
        return self.currentState
    def set_state(self, state):
        self.currentState = state

if __name__ == '__main__':
    game = Game()
    game.run()