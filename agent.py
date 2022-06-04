import torch
import random
import numpy as np
from collections import deque
from game import CarGameAI, Direction, Point
from model import Linear_QNet, QTrainer
from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(7, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        head = game.car[0]
        #head = game.head

        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y + 20)
        
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        state = [
            # Danger straight
            (dir_r and game.is_collision(point_r)) or
            (dir_l and game.is_collision(point_l)) or
            (dir_u and game.is_collision(point_u)) or
            (dir_d and game.is_collision(point_d)),

            # Danger right
            (dir_u and game.is_collision(point_r)) or
            (dir_d and game.is_collision(point_l)) or
            (dir_l and game.is_collision(point_u)) or
            (dir_r and game.is_collision(point_d)),

            # Danger left
            (dir_d and game.is_collision(point_r)) or
            (dir_u and game.is_collision(point_l)) or
            (dir_r and game.is_collision(point_u)) or
            (dir_l and game.is_collision(point_d)),

            # food straight
            (dir_r and game.food.x > game.head.x) or
            (dir_l and game.food.x < game.head.x) or
            (dir_u and game.food.y < game.head.y) or
            (dir_d and game.food.y > game.head.y),

            # food right
            (dir_u and game.food.x > game.head.x) or
            (dir_d and game.food.x < game.head.x) or
            (dir_l and game.food.y < game.head.y) or
            (dir_r and game.food.y > game.head.y),

            # food left
            (dir_d and game.food.x > game.head.x) or
            (dir_u and game.food.x < game.head.x) or
            (dir_r and game.food.y < game.head.y) or
            (dir_l and game.food.y > game.head.y),
            # food back
            (dir_d and game.food.y < game.head.y) or
            (dir_u and game.food.y > game.head.y) or
            (dir_r and game.food.x < game.head.x) or
            (dir_l and game.food.x > game.head.x)
            ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0

    agent = Agent()
    game = CarGameAI()


    print("starting")
    while True:
        # get old state
        state_old = agent.get_state(game)

        print(state_old)
        # get move
        final_move = agent.get_action(state_old)

        #print(final_move)
        #perform move and get new state
        reward, done, score = game.play_step(final_move)

        state_new = agent.get_state(game)


        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)


        # remember
        agent.remember(state_old, final_move, reward, state_new, done)


        if done:
            # train long memory, plot result
            game.reset()

            agent.n_games += 1

            agent.train_long_memory()


            if score > record:
                record = score
                agent.model.save()


            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    train()