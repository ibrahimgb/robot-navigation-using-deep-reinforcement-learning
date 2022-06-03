import pygame
import random
from enum import Enum
from collections import namedtuple
from helper import plot

pygame.init()
font = pygame.font.Font('arial.ttf', 25)


# font = pygame.font.SysFont('arial', 25)

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
BLACK = (128,128,128)
GREY1 = (128,200,0)
GREY2 = (200,200,0)
BLOCK_SIZE = 20
SPEED = 20


class CarGameAStar:

    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w / 2, self.h / 2)
        self.car = [self.head]
        self.obstacle = []
        self.score = 0
        self.food = None
        self._place_food()
        self.plot_scores = []
        self.plot_mean_scores = []
        self.n_games = 1
        self.scores = []

    def _place_obstacle(self):#t gole need to change
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        obstacle = Point(x, y)

        if obstacle in self.obstacle or self.head == obstacle or self.food == obstacle:
            self._place_obstacle()
        self.obstacle.append(obstacle)



    def _place_food(self):  # t gole need to change
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.car:
            self._place_food()

        self.frame_iteration = 0
        self._place_obstacle()
        print("this is coooooooooooooooooooooooooooooooooooooooooooooooool")

    def reset(self):

        self.plot_scores.append(score)
        total_score = sum(self.scores)
        mean_score = total_score / self.n_games
        self.plot_mean_scores.append(mean_score)
        plot(self.plot_scores, self.plot_mean_scores)


        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w / 2, self.h / 2)
        self.car = [self.head]
        self.n_games = self.n_games + 1
        self.scores.append(self.score)
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0
        self.obstacle = []
        #self.first_time = True

    def play_step(self):
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN


        # 2. move
        self._move(self.direction)  # update the head
        self.car.insert(0, self.head)

        # 3. check if game over
        game_over = False
        if self.is_collision():
            self.reset()

            return game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
            self.car.pop()
        else:
            self.car.pop()

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return game_over, self.score

    def is_collision(self, pt=None):
        #print(self.frame_iteration)

        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            self.reset()
            return True
        # if self.head in self.obstacle:
        if pt in self.obstacle:  #########################################""
            return True

        if pt in self.car[1:]:
            return True

        return False

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.car:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))
        for pt in self.obstacle:
            pygame.draw.rect(self.display, GREY1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, GREY2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if self.food.x > self.head.x:
            x += BLOCK_SIZE
        elif self.food.x < self.head.x:
            x -= BLOCK_SIZE
        elif self.food.y > self.head.y:
            y += BLOCK_SIZE
        elif self.food.y < self.head.y:
            y -= BLOCK_SIZE

        self.head = Point(x, y)




if __name__ == '__main__':
    game = CarGameAStar()

    # game loop
    while True:
        game_over, score = game.play_step()

        if game_over == True:
            break

    print('Final Score', score)

    pygame.quit()