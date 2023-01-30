import pygame
from pygame.math import Vector2
from pygame.locals import *
import random
import sys
import time


class Snake:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_block = False

#------------------------------------------IMAGES--------------------------------------------------------------------
        
        self.head_up = pygame.image.load(r'D:\User Files\Programming\.Projects\Snake Game\img\head_up.png').convert_alpha()
        self.head_down = pygame.image.load(r'D:\User Files\Programming\.Projects\Snake Game\img\head_down.png').convert_alpha()
        self.head_right = pygame.image.load(r'D:\User Files\Programming\.Projects\Snake Game\img\head_right.png').convert_alpha()
        self.head_left = pygame.image.load(r'D:\User Files\Programming\.Projects\Snake Game\img\head_left.png').convert_alpha()

        self.tail_up = pygame.image.load(r'D:\User Files\Programming\.Projects\Snake Game\img\tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load(r'D:\User Files\Programming\.Projects\Snake Game\img\tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load(r'D:\User Files\Programming\.Projects\Snake Game\img\tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load(r'D:\User Files\Programming\.Projects\Snake Game\img\tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load(r'D:\User Files\Programming\.Projects\Snake Game\img\body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load(r'D:\User Files\Programming\.Projects\Snake Game\img\body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load(r'.Projects\Snake Game\img\body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load(r'D:\User Files\Programming\.Projects\Snake Game\img\body_tl.png').convert_alpha()
        self.body_br = pygame.image.load(r'D:\User Files\Programming\.Projects\Snake Game\img\body_br.png').convert_alpha()
        self.body_bl = pygame.image.load(r'D:\User Files\Programming\.Projects\Snake Game\img\body_bl.png').convert_alpha()
        self.crunch_sound = pygame.mixer.Sound(r'D:\User Files\Programming\.Projects\Snake Game\sound\crunch.wav')
#------------------------------------------IMAGES--------------------------------------------------------------------
        
       
    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()


        for index,block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)

            if index == 0:
                screen.blit(self.head,block_rect)  

            elif index == len(self.body) - 1:
                screen.blit(self.tail,block_rect)

            else:
                previous_block = self.body[index+1] - block
                next_block = self.body[index-1] - block
                
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical,block_rect)
                
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal,block_rect)

                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl,block_rect)

                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl,block_rect)

                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr,block_rect)

                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br,block_rect)


    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1,0): self.head = self.head_right
        elif head_relation == Vector2(0,1): self.head = self.head_up
        elif head_relation == Vector2(0,-1): self.head = self.head_down


    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0):
            self.tail = self.tail_left
        if tail_relation == Vector2(-1,0):
            self.tail = self.tail_right
        if tail_relation == Vector2(0,1):
            self.tail = self.tail_up
        if tail_relation == Vector2(0,-1):
            self.tail = self.tail_down


    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]


    def add_block(self):
        self.new_block = True


    def play_crunch_sound(self):
        self.crunch_sound.play()


    def reset(self):
        pass




class Fruit:
    def __init__(self):
        self.randomize()


    def draw_fruit(self):
        
        fruit_rect = pygame.Rect(int(self.pos.x*cell_size),int(self.pos.y*cell_size),cell_size,cell_size)
        screen.blit(apple,fruit_rect)


    def randomize(self):
        self.x = random.randint(0,cell_number-1)
        self.y = random.randint(0,cell_number-1)
        self.pos = Vector2(self.x,self.y)



class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()


    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()


    def draw_elements(self):
        self.grass_draw()
        self.snake.draw_snake()
        self.fruit.draw_fruit()
        self.draw_score()


    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
            
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
                


    def game_over(self):
        gFont = pygame.font.SysFont('Arial Black', 72)
        GOsurf = gFont.render('Game over!', True, (255,0,0))
        GOrect = GOsurf.get_rect()
        GOrect.midtop = (360, 15)
        screen.blit(GOsurf, GOrect)
        
        pygame.display.flip()

        time.sleep(2)
        pygame.quit()
        sys.exit()


    def grass_draw(self):
        grass_color = (167,209,61)
        for row in range(cell_number):
            if row % 2 ==0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size,row * cell_size , cell_size , cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)
            
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size,row * cell_size , cell_size , cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)

    
    def draw_score(self):
        with open(r'.Projects\Snake Game\score.txt','r') as score:
            high_score = score.read()


        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text,True,(56,74,112))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        apple_rect = apple.get_rect(midright = (score_rect.left,score_rect.centery))

        score_high = str("HI: "+high_score)
        score_high_surface = game_font.render(score_high,True,(56,74,112))
        score_high_rect = score_high_surface.get_rect(center = (40,20))
        screen.blit(score_high_surface,score_high_rect)

        bg_rect = pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width + score_rect.width + 4, apple_rect.height)
        pygame.draw.rect(screen,(167,209,61),bg_rect)
        screen.blit(score_surface,score_rect)
        screen.blit(apple,apple_rect)
        pygame.draw.rect(screen,(56,74,112),bg_rect,2)

        if int(score_text) > int(high_score):
            with open(r'D:\User Files\Programming\.Projects\Snake Game\score.txt','w') as score:
                score.write(score_text)


    def reset_score(self):
        with open(r'D:\User Files\Programming\.Projects\Snake Game\score.txt','w') as score:
            score.write("0")



pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()

cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_size*cell_number,cell_size*cell_number))

game_font = pygame.font.Font(r'D:\User Files\Programming\.Projects\Snake Game\font\PoetsenOne-Regular.ttf',25)

clock = pygame.time.Clock()

apple = pygame.image.load(r"D:\User Files\Programming\.Projects\Snake Game\img\apple.png")



SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,90)
main_game = Main()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == SCREEN_UPDATE:
            main_game.update()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            
            
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0,-1)


            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1,0)


            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0,1)


            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1,0)


            if event.key == pygame.K_r:
                main_game.reset_score()
    
                
    screen.fill((175,215,70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
    
        