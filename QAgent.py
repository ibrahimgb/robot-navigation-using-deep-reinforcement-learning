import torch
import random
import numpy as np
from collections import deque
from game2 import CarGameAI, Direction, Point
from model import Linear_QNet, QTrainer
from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent:

    def __init__(self):
        self.n_games = 0


    def get_state(self, game):
        head = game.car[0]
        # head = game.head

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

        stateInt = np.array(state, dtype=int)

        stateToReturn = (stateInt[0],stateInt[1],stateInt[2],stateInt[3],stateInt[4]
                         ,stateInt[5],stateInt[6])
        #print(stateToReturn)
        return stateToReturn


def max_action(Q, state, actions=[0,1,2]):
    values = np.array([Q[state,a] for a in actions])
    #print(values)
    action = np.argmax(values)

    return action



if __name__ == '__main__':

    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0

    n_games = 50000
    alpha = 0.1
    gamma = 0.99
    eps = 1.0

    action_space =  [0,1,2]# [[0,1,0],[1,0,0],[0,0,1]]

    # dangerStraight
    # dangerRight
    # dangerLeft
    # foodLocationL
    # foodLocationR
    # foodLocationB
    # foodLocationF

    states = []
    for dangerStraight in range(2):
        for dangerRight in range(2):
            for dangerLeft in range(2):
                for foodLocationL in range(2):
                    for foodLocationR in range(2):
                        for foodLocationB in range(2):
                            for foodLocationF in range(2):
                                states.append((dangerStraight , dangerRight , dangerLeft , foodLocationL , 
                                               foodLocationR , foodLocationB , foodLocationF))



    Q = {}
    for state in states:
        for action in action_space:
            Q[state, action] = 0

    score = 0
    #print(states)
    total_rewards = np.zeros(n_games)
    
    for i in range(n_games):
        done = False 
        game = CarGameAI()
        agent = Agent()
        state = agent.get_state(game)
        score = 0
        #if i % 50 == 0 and i > 0:
            #print('episode ', i, 'score ', score, 'epsilon %.3f' % eps)
        values = np.array([Q[state, a] for a in [0,1,2]])
        while not done:

            action = np.random.choice([0,1,2]) if np.random.random() < eps \
                    else max_action(Q, state)
            reward, done, score = game.play_step_helper(action)
            obs_ = agent.get_state(game)
            score = game.score
            state_ = agent.get_state(game)
            score += reward

            action_ = max_action(Q, state_)

            Q[state, action] = Q[state, action] + alpha*(reward + gamma*Q[state_, action_] - Q[state, action])
            state = state_
        total_rewards[i] = score
        eps = eps - 2/n_games if eps > 0.01 else 0.01

    mean_rewards = np.zeros(n_games)
    for t in range(n_games):
        mean_rewards[t] = np.mean(total_rewards[max(0, t-50):(t+1)])
    #plt.plot(mean_rewards)
    #plt.savefig('mountaincar.png')

    #f = open("mountaincar.pkl","wb")
    #pickle.dump(Q,f)
    #f.close()

    if done:
        # train long memory, plot result
        game.reset()

        if score > record:
            record = score
            agent.model.save()

        print('Game', agent.n_games, 'Score', score, 'Record:', record)

        plot_scores.append(score)
        total_score += score
        mean_score = total_score / agent.n_games
        plot_mean_scores.append(mean_score)
        plot(plot_scores, plot_mean_scores)
