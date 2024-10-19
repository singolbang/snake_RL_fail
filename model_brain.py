
import torch
from numba import float64
from torch import nn
from torch.nn.functional import linear
from torch import optim
import tkinter
from snake_game import *
from collections import deque
import random

class Brain(nn.Module):
    def __init__(self):
        super(Brain, self).__init__()

        self.conv2d = nn.Sequential(nn.Conv2d(3, 16, stride = 2 ,kernel_size=2),
                                    nn.BatchNorm2d(16), nn.ReLU(),)
                                    #nn.Conv2d(16, 32, stride = 2 ,kernel_size=2),
                                    #nn.BatchNorm2d(32),nn.ReLU(),
                                   # nn.Conv2d(32, 32, stride = 2 ,kernel_size=2),
                                    #nn.BatchNorm2d(32), nn.ReLU())

        self.pool = nn.AdaptiveMaxPool2d((1,1))
        self.fc = nn.Sequential(nn.Linear(16, 16), nn.ReLU(),
                                nn.Linear(16, 8), nn.ReLU(),
                                nn.Linear(8, 4), nn.Softmax())


    def forward(self, x):
        x = self.conv2d(x)
        x = self.pool(x)
        x = torch.flatten(x, 1)
        x = self.fc(x)

        return x

class ReplayMemory:
    def __init__(self, capacity):
        self.memory = []
        self.capacity = capacity
        self.position = 0

    def push(self, state, action, reward, next_state, done):
        if len(self.memory) < self.capacity:
            self.memory.append(None)
        self.memory[self.position] = (state, action, reward, next_state, done)
        self.position = (self.position + 1) % self.capacity

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)

'''

def train_model(game, Q_network, target_network, memory, optimizer,loss_f, gamma, batch_size=64):
    if len(memory) < batch_size:
        return False

    # 경험 배치 샘플링
    batch = memory.sample(batch_size)
    states, actions, rewards, next_states, dones = zip(*batch)

    states = torch.stack(states)
    actions = torch.tensor(actions)
    next_states = torch.stack(next_states)

    #inputs = torch.zeros((min(len(memory), batch_size)), states.shape[1], states.shape[2])
    #targets = torch.zeros((min(len(memory), batch_size)), states.shape[1], states.shape[2])

    # Q값 계산
    Q_values = Q_network(states)
    Q_value = Q_values.gather(1, actions.unsqueeze(1))

    with torch.no_grad():
        next_Q_values = target_network(next_states)
        next_Q_value,_ = torch.max(next_Q_values, dim = 1)

    if not dones:
        Q = torch.tensor(rewards).float() + gamma * next_Q_value
    else:
        Q = torch.tensor(rewards).float()
    #print(Q)
    loss = loss_f(Q_value, Q)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    return loss.item()

'''




