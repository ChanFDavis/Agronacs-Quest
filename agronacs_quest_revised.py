# Revision began on 9/5/2018
import pygame, random, os

level_directory = "levels/"
picked_level = random.choice(os.listdir(level_directory))

level_title = picked_level.rstrip(".txt")

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (165, 165, 165)
RED = (200, 0, 0)
GREEN = (0, 255, 0)
BLUE = (75, 175, 200)
GOLD = (200, 210, 0)
PURPLE = (255, 0, 255)

PLAYER = (0,25,12,25)
PLAYER_2 = (13, 25, 12, 25)
STONE = (50,0,25,25)
STONE_PLATFORM = (75, 25, 25, 14)
GRASS = (0,0,25,25)
GRASS_PLATFORM = (50, 25, 25, 14)
LAVA = (25,0,25,25)
SPIKES = (75,0,25,25)
COIN_BIG = (25,25,12,25)
COIN_SMALL = (38, 25, 12, 12)

_game_end = False
global _score_to_win

score_font = pygame.font.SysFont('ocraextended', 12, False, False)
endgame_message_font = pygame.font.SysFont('magneto', 30, True, False)

win_message = endgame_message_font.render("Congrats, you won!", True, BLACK)
lose_message = endgame_message_font.render("Dang, you lost!", True, BLACK)

level_file = open(level_directory + picked_level)

tile_list = []

for line in level_file:
    line = line.strip()
    tile_list.append(line)

def check_if_won():
    global _game_end
    if _score == _score_to_win:
        _game_end = True
        _player.dx = 0
        return True
    
def check_if_lost():
    
    global size
    
    hazard_hit_list = pygame.sprite.spritecollide(_player, hazard_list, False)
    
    if (len(hazard_hit_list) > 0) or (_player.rect.y > size[1]): 
        _player.kill()        
        return True

class SpriteSheet(object):
    sprite_sheet = None
    
    def __init__(self, sprite_sheet):
        
        self.sprite_sheet = pygame.image.load(sprite_sheet).convert()
        
    def get_image(self, x, y, width, height):
        
        image = pygame.Surface([width, height]).convert()
        
        image.blit(self.sprite_sheet, (0,0), (x, y, width, height))
        
        image.set_colorkey(GREEN)
        
        return image
    

_score = 0
_score_to_win = 0
_player = None


        
# Divider

class Tile(pygame.sprite.Sprite):
    
    def __init__(self, sprite_sheet_data, x, y):
        
        pygame.sprite.Sprite.__init__(self)
        
        sprite_sheet = SpriteSheet('sprite_sheet.png')
        
        self.image = sprite_sheet.get_image(sprite_sheet_data[0], sprite_sheet_data[1], sprite_sheet_data[2], sprite_sheet_data[3])
        
        self.rect = self.image.get_rect()
        
        self.rect.x = x
        self.rect.y = y


    
def make_from_file(tile_list):
    """
    Creates a 2d grid of characters from a list of strings.
    All strings must be the same length.
    """
    grid = []
    rows = len(tile_list)
    for row in range(0, rows):
        row_elements = []
        cols = len(tile_list[row])
        for col in range(0, cols):
            row_elements.append(tile_list[row][col])
        grid.append(row_elements)
    return grid

def which_tile(row, col):
    if level[row][col] == "-":
        pass
    
    elif level[row][col] == "G":
        tile = Tile(GRASS, col * 25, row * 25)
        platform_list.add(tile)
        all_sprites.add(tile)
        
    elif level[row][col] == "g":
        tile = Tile(GRASS_PLATFORM, col * 25, row * 25)
        platform_list.add(tile)
        all_sprites.add(tile)  
    
    elif level[row][col] == "L":
        tile = Tile(LAVA, col * 25, row * 25)
        hazard_list.add(tile)
        all_sprites.add(tile)
        
    elif level[row][col] == "S":
        tile = Tile(STONE, col * 25, row * 25)
        platform_list.add(tile)
        all_sprites.add(tile) 
        
    elif level[row][col] == "s":
        tile = Tile(STONE_PLATFORM, col * 25, row * 25)
        platform_list.add(tile)
        all_sprites.add(tile)    
        
    elif level[row][col] == "o":
        tile = Tile(COIN_SMALL, (col * 25) + 6, row * 25)
        coin_list.add(tile)
        all_sprites.add(tile)  
        
    elif level[row][col] == "^":
        tile = Tile(SPIKES, col * 25, row * 25)
        hazard_list.add(tile)
        all_sprites.add(tile) 
        
    elif level[row][col] == "c":
        pass
        
    elif level[row][col] == "*":
        global _player
        _player = Player(PLAYER_2, 0, 0)
        _player.rect.x = 25 * col
        _player.rect.y = 25 * row
        player_list.add(_player)
        
# The class of the controllable player
class Player(pygame.sprite.Sprite):
    
    dx = 0
    dy = 0
        
    def __init__(self, sprite_sheet_data, x, y):        
        pygame.sprite.Sprite.__init__(self)
        sprite_sheet = SpriteSheet('sprite_sheet.png')
        
        self.image = sprite_sheet.get_image(sprite_sheet_data[0], sprite_sheet_data[1], sprite_sheet_data[2], sprite_sheet_data[3])
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def get_movement(self, x, y):
        self.dx += x
        
    def update(self):
        
        self.get_gravity()
        self.rect.x += self.dx
        block_list = pygame.sprite.spritecollide(self, platform_list, False)
        
        for block in block_list:
            if self.dx > 0:
                self.rect.right = block.rect.left
            elif self.dx < 0:
                self.rect.left = block.rect.right            
        
        self.rect.y += self.dy
            
        block_list = pygame.sprite.spritecollide(self, platform_list, False)
    
        for block in block_list:  
            if self.dy > 0:
                self.rect.bottom = block.rect.top
            elif self.dy < 0:
                self.rect.top = block.rect.bottom
                self.dy = 0
            self.dy =0
        
        coin_collect_list = pygame.sprite.spritecollide(self, coin_list, True)
        for coin in coin_collect_list:
            global _score
            _score += 1
            
    def get_gravity(self):
        if self.dy == 0:
            self.dy = .5
        else:
            self.dy += .35
    
    def jump(self):
        
        global size
        self.rect.y += 2
        jump_test = pygame.sprite.spritecollide(self, platform_list, False)
        self.rect.y -= 2
        
        if len(jump_test) > 0:
            self.dy = -6 

level = make_from_file(tile_list)

size = (25 * len(level[0]), 25 * len(tile_list))

screen = pygame.display.set_mode(size)

player_list = pygame.sprite.Group()
platform_list = pygame.sprite.Group()
coin_list = pygame.sprite.Group()
hazard_list = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

for row in range(0 , len(level)):
#    global _score_to_win
    
    _score_to_win += level[row].count('o')

    for col in range(0, len(level[0])):
        which_tile(row, col)

pygame.display.set_caption("Agronac's Quest: " + level_title)

clock = pygame.time.Clock()
done = False
while not done:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.KEYDOWN and _game_end == False:
            if event.key == pygame.K_SPACE:
                _player.jump()
            
            if event.key == pygame.K_d:
                _player.get_movement(3, 0)
                sprite_sheet = SpriteSheet('sprite_sheet.png')
                sprite_sheet_data = PLAYER_2
                _player.image = sprite_sheet.get_image(sprite_sheet_data[0], sprite_sheet_data[1], sprite_sheet_data[2], sprite_sheet_data[3])                
            elif event.key == pygame.K_a:
                _player.get_movement(-3, 0)
                sprite_sheet = SpriteSheet('sprite_sheet.png')
                sprite_sheet_data = PLAYER
                _player.image = sprite_sheet.get_image(sprite_sheet_data[0], sprite_sheet_data[1], sprite_sheet_data[2], sprite_sheet_data[3])
                

        elif event.type == pygame.KEYUP and _game_end == False:
            if event.key == pygame.K_d:
                _player.get_movement(-3, 0)
            elif event.key == pygame.K_a:
                _player.get_movement(3, 0)   
    
    screen.fill(BLUE)
    
    all_sprites.update() 
    all_sprites.draw(screen)
    player_list.update()    
    player_list.draw(screen)
    
    score_text = score_font.render("Score: " + str(_score), True, BLACK)    
    screen.blit(score_text, [0, 0])
    
    if check_if_won() == True:
        screen.blit(win_message, [size[0]/2 - 175, size[1]/2])
    
    if check_if_lost() == True:
        screen.blit(lose_message, [size[0]/2 - 125, size[1]/2])
    

    clock.tick(60)    
    
    pygame.display.flip()
    
    
    
pygame.quit()
