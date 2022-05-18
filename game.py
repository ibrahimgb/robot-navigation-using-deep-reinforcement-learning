import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.Font('arial.ttf', 25)
#font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (0,255,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
GREY1 = (128,200,0)
GREY2 = (200,200,0)
BLACK = (128,128,128)

BLOCK_SIZE = 20
SPEED = 40

class CarGameAI:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        #self.first_time = True
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Car Nav')
        self.clock = pygame.time.Clock()
        self.obstacle= []
        self.reset()



    def reset(self):
        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.car = [self.head]

        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0
        self.obstacle = []
        #self.first_time = True



    def _place_food(self):#t gole need to change
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.car:
            self._place_food()

        self.frame_iteration = 0
        self._place_obstacle()
        print("this is coooooooooooooooooooooooooooooooooooooooooooooooool")


    def _place_obstacle(self):#t gole need to change
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        obstacle = Point(x, y)

        if obstacle in self.obstacle or self.head == obstacle or self.food == obstacle:
            self._place_obstacle()
        self.obstacle.append(obstacle)



    def play_step(self, action):
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # 2. move
        self._move(action) # update the head
        self.car.insert(0, self.head)


        # 3. check if game over
        reward = 0
        game_over = False

        if self.is_collision() or self.frame_iteration > 100*len(self.car):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
            self.car.pop()
        else:
            self.car.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return reward, game_over, self.score


    def is_collision(self, pt=None):
        print(self.frame_iteration)
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        #if self.head in self.obstacle:
        if pt in self.obstacle:#########################################""
            return True

        if pt in self.car[1:]:
            return True

        return False

    def _update_ui(self):
        self.display.fill(BLACK)
        #print(self.snake)
        #print(self.obstacle)
        for pt in self.car:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
        for pt in self.obstacle:
            pygame.draw.rect(self.display, GREY1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, GREY2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()


    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)

