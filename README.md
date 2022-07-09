# Robot Navigation In Dynamic Maze Using Deep Reinforcement Learning


Navigation and obstacle avoidance for mobile robots in an unknown environment is a critical issue in autonomous robotics. Navigation in an unknown environment is a reinforcement learning (RL) problem because the best navigation plan can only be discovered through trial-and-error interaction with the environment.
By achieving the ideal Q-value function that offers the best results for all states, RL tries to train the agent how to act in an unknown environment. The agent updates Q-values for optimality convergence using rewards acquired from the environment after action selections for each state.
In this regard, researchers have looked into a number of techniques for robot navigation path planning. In this post, we've tried to look at a variety of topics.In this study, we'll look at two different Reinforcement Learning approaches, as well as navigation techniques. Q-learning and deep  Q-Learning.

# Environment


The environment for this problem is a grid with obstacles and a single goal. the agent is placed randomly (in an unoccupied cell) in the environment. The agent goal is to reach the goal cell as quickly as possible. To get there the agent moves through the cells in a succession of steps. For every step, the agent must decide which action to take (move left/right/forward). For this purpose the agent is trained; it learns a policy that tells what is the best next move to make. With every step, the agent incurs a penalty or (when finally reaching the exit) a reward. These penalties and rewards are the input when training the policy.

 A invierment (2d grid) with obstcels. A Robot is placed at the start cell (random sell) and must find the goal cell by moving through.
Empty cells are where the robot can move, a cell that contains an obstacle and cannot be entered which is detected by the senses of the robot and if the robot crashes it will restart, robotPos cell indicates the current position of the robot, and the rules how to move through it are called the environment. A robot is placed
at the start cell. The robot chooses actions (move left/right/forward) in order to reach the Goal-cell. 
 Every action results in a reward or penalty  Every move gives a small penalty (-1) and running into an obstacle a large penalty (-100). The reward (+100) is collected when the agent reaches the Goal. 
 
 
reaching the goal in the terminal state means winning; the robot either wins or loses. 
the robot starts in a simple environment (with 20 obstacles) and for every successful operation (retching the goal) the reboot will get reassigned to another goal (destination) and the other obstacle is added to the environment.

# Model

## Qtable model


The q-table model is applied on an enviermant, grid with the agents’ starting position at the senter.
the robot starts to navigate in space drawing an optimal path on its way to the goal.
Upon completion of the training , the model generate a table with all the possible use cases 128 possible observations. and tweek the q value depending on the reword (feedback)


## QNetwork Model

This model is applied on an enviermant, grid with the agents’ starting position at the center.
prediction model uses Q-learning and a neural network.  The training algorithm ensures
that the robot starts from every possible cell. Training ends after a fixed number
of episodes, or earlier if a stopping criterion is reached. As an extra feature after learning it saves the model to disk so this can be loaded later for the next episode.


# Robot Input Output


## Robot Observations
the robot has observations or inputs, 7 observations. to simplify the problem the inputs
are binary (is Danger straight, is Danger right, is Danger left, the goal is straight , goal is right
, goal is left, goal is back) in reality the goal direction can be with a GPS or other localization
methods mentioned previously, and the obstacle sensors will gonna use ultrasonic sensors or
Reflective proximity sensors. those inputs will ganna be fed to our agents to generate actions.
## Robot Actions
the robot can take action fed to it from the neural network. the actions are: keep moving
forward, move left, move right. the robot can do only one action and can’t do tow at the
same time.
the observations of the robot are (no Danger straight, no Danger right, no Danger left,
goal is straight , goal is not right , goal is left, goal is not back). or we can represent it with
an list: [0,0,0,1,0,1,0]
# Q Lerning Resultas
![Qlerning-resultats (1)](https://user-images.githubusercontent.com/59414164/178087648-048eb1d5-706c-437d-8491-774e29e14efb.png)

# Deep Q Lerning Resultas

![DQL resutlas (1)](https://user-images.githubusercontent.com/59414164/178087701-d6c5ddcb-b698-409c-8871-5d3dfe54e9d3.png |width=200px)




# Discussion
Deep Q Learning and Q Learning are both Reinforcement Learning, Model Free, Value-
Based, Off Policy Models. in our comparison we used for both algorithms the same envi-
ronment where we provided the model with the exact same inputs (observations) and same
outputs(Actions). in all the cases the Deep Q Learning model outperformed the Q Learning
model, with a mean of 1836 successful sequential operations without crashing. and 136 for
the Q Learning model with a max of 89 successful sequential operations without crashing In an empty environment. in the complex environment, the deep q learning model scored an
average of 28 successful operations, for the Q Learning model scored a mean of 18 successful
operations.
that aside Deep Q Learning performed 64% better than Q Learning.
for the relay memory, the content stored in it influences the performance of the model,
if the number of the unsuccessful operations in it exceeds the number of successful oper-
ations the performance of the model will increase, which means the DQL model learns from
its mistakes, and if the relay memory has only successful operations stored in the memory
the model won’t avoid crashing into obstacles and seeks a direct path to the goal only to
maximize the reward (it’s won’t take into consideration the penalty cracking into an obsta-
cle). DQL can adopt a smart behavior like wall following to retch the goal and that has not
been observed in the Q Learning model.

# Conclusion
Real-time (or simulated) learning algorithms can tackle the problem of mobile robot nav-
igation and learn a good policy. When the robot was tested with a new start new grid,
the performance of the two approaches differed depending on the environment. DQN robot
outperformed Q-learning in terms of overall performance, owing to Deep Qlearning capacity
to handle more complex environments and higher generalization ability to navigate than QL.
Q-Learning is required as a pre-requisite as it is a process of Q-Learning creates an exact
matrix for the working agent which it can “refer to” to maximize its reward in the long
run. Although this approach is not wrong in itself, this is only practical for very small
environments and quickly loses it’s feasibility when the number of states and actions in the
environment increases.
Thus, this thinking leads us to Deep Q-Learning which uses a deep neural network to
approximate the values. This approximation of values does not hurt as long as the relative
importance is preserved. The basic working step for Deep Q-Learning is that the initial state
is fed into the neural network and it returns the Q-value of all possible actions as an output.
a classic Q-table is not very scalable. It might work for simple envierments, but in a more
complex envierment with dozens of possible actions and game states the Q-table will soon
get complex and cannot be solved efficiently anymore.


