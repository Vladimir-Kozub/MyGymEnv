import numpy as np

from gym import Env, spaces
from gym.utils import seeding

def categorical_sample(prob_n, np_random):
    """
    Sample from categorical distribution
    Each row specifies class probabilities
    """
    prob_n = np.asarray(prob_n)
    csprob_n = np.cumsum(prob_n)
    return (csprob_n > np_random.rand()).argmax()


class Snake(Env):

    """
    Has the following members
    - nS: number of states
    - nA: number of actions
    - P: transitions (*)
    - isd: initial state distribution (**)

    (*) dictionary dict of dicts of lists, where
      P[s][a] == [(probability, nextstate, reward, done), ...]
    (**) list or array of length nS


    """
    def __init__(self, X, Y):
        self.FieldShape = [X,Y]
        self.reset()

        self.lastaction = None # for rendering

        self.nA = 4

        self.action_space = spaces.Discrete(self.nA)

    def reset(self):
        self.SnakeLen = 0
        self.SnakePos = [[np.random.choice(self.FieldShape[0]), np.random.choice(self.FieldShape[1])]]
        self.FrutPos = self.generate_new_frut_pos()
        self.s = ''
        for i in self.SnakePos:
            self.s += str(i[0]) + str(i[1])
        self.s += str(self.FrutPos[0]) + str(self.FrutPos[1])
        self.s = int(self.s)
        return  self.s

    def step(self, a):
        # transitions = self.P[self.s][a]
        # i = categorical_sample([t[0] for t in transitions], self.np_random)
        # p, s, r, d= transitions[i]
        # self.s = s
        # self.lastaction = a
        #print(1)
        done = False
        new_pos = list(self.SnakePos[self.SnakeLen])
        new_pos[a%2]+= 1 - 2*(a//2)
        if np.array_equal(new_pos, self.FrutPos):
            self.SnakePos.append(new_pos)
            reward = sum(self.FieldShape)
            self.SnakeLen +=1
            self.FrutPos = self.generate_new_frut_pos()
        else:
            reward = -1
            if (new_pos[a%2] < 0) or (new_pos[a%2] > self.FieldShape[a%2]) or (new_pos in self.SnakePos):
                done = True
                reward = -max(self.FieldShape)
                self.lastaction = a
            else:
                #print(self.SnakePos, new_pos)
                self.SnakePos.append(new_pos)
                del(self.SnakePos[0])
        self.s = ''
        for i in self.SnakePos:
            self.s += str(i[0]) + str(i[1])
        self.s += str(self.FrutPos[0]) + str(self.FrutPos[1])
        self.s = int(self.s)
        return (self.s, reward, done)



    def render(self, mode='human'):
        for i in range(self.FieldShape[1]):
            s = ''
            for j in range(self.FieldShape[0]):
                if [j,i] in self.SnakePos:
                    s+='S'
                else:
                    if [j,i] ==self.FrutPos:
                        s+='F'
                    else:
                        s+='*'

            print(s)

    def generate_new_frut_pos(self):
        new_frut_pos = [np.random.choice(self.FieldShape[0]), np.random.choice(self.FieldShape[1])]
        while new_frut_pos in self.SnakePos:
            new_frut_pos = [np.random.choice(self.FieldShape[0]), np.random.choice(self.FieldShape[1])]
        return new_frut_pos
