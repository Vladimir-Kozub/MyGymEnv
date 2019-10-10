import numpy as np
import sys
from six import StringIO

from gym import spaces, utils
from gym.envs.toy_text import discrete

MAP = [
    "|---------|",
    "| | | | | |",
    "| | | | | |",
    "| | | | | |",
    "| | | | | |",
    "| | | | | |",
    "|---------|",
]

class Snake(discrete.DiscreteEnv):

    metadata = {'render.modes': ['human']} #, 'ansi'



    def __init__(self, size):
        self.X = size
        self.Y = size

        nS = (self.X * self.Y)**2
        nR = self.Y
        nC = self.X
        nfR = self.Y
        nfC = self.X
        isd = np.zeros(nS)
        nA = 4
        P = {s : {a : [] for a in range(nA)} for s in range(nS)}
        for snakerow in range(nR):
            for snakecol in range(nC):
                for frutrow in range(nfR):
                    for frutcol in range(nfC):
                        # state = self.encode(row, col, passidx, destidx)
                        # if passidx < 4 and passidx != destidx:
                        #     isd[state] += 1
                        for a in range(nA):
                            reward = -1
                            if a==0:
                                new_snakerow = max(0, snakerow-1)
                                new_snakecol = snakecol
                            if a==1:
                                new_snakerow = snakerow
                                new_snakecol = min(snakecol+1, self.X - 1)
                            if a==2:
                                new_snakerow = min(self.Y-1, snakerow+1)
                                new_snakecol = snakecol
                            if a==3:
                                new_snakerow = snakerow
                                new_snakecol = max(0, snakecol-1)
                            if (frutcol == new_snakecol and frutrow == new_snakerow):
                                #print('Yes')
                                reward = 9
                                tmp = nfR*nfC -1
                                for i in range(nfR):
                                    for j in range(nfC):
                                        if (i != new_snakerow and j != new_snakecol):
                                            new_state = self.encode(new_snakerow, new_snakecol, i, j)
                                            state = self.encode(snakerow, snakecol, frutrow, frutcol)
                                            P[state][a].append(
                                                (1.0/tmp, new_state, reward, False))
                                # new_frutrow = [0,1,2,3,4]
                                # new_frutrow.remove(frutrow)
                                # new_frutcol = [0, 1, 2, 3, 4]
                                # new_frutcol.remove(frutcol)
                                # new_frutrow = np.random.choice(a = new_frutrow)
                                # new_frutcol = np.random.choice(a = new_frutcol)

                            else:
                                new_frutcol = frutcol
                                new_frutrow = frutrow
                                new_state = self.encode(new_snakerow, new_snakecol, new_frutrow, new_frutcol)
                                state = self.encode(snakerow, snakecol, frutrow, frutcol)
                                P[state][a].append(
                                    (1.0, new_state, reward, False))
                                isd[self.encode(new_snakerow, new_snakecol, new_frutrow, new_frutcol)] += 1
        isd /= isd.sum()
        discrete.DiscreteEnv.__init__(self, nS, nA, P, isd)

    def encode(self, taxirow, taxicol, frutrow, frutcol):
        i = (taxirow*self.X + taxicol)*self.X*self.Y + (frutrow*self.X + frutcol)
        return i

    def decode(self, i):
        out = []
        out.append((i % (self.X*self.Y)) % self.X)
        out.append((i % (self.X*self.Y))//self.X)
        i = i // (self.X*self.Y)
        out.append(i % self.X)
        out.append(i// self.X)
        return reversed(out)

    def render(self, mode='human'):
        dec = list(self.decode(self.s))
        for i in range(self.Y):
            s = ''
            for j in range(self.X):
                if i == dec[0] and j == dec[1]:
                    s += 'S'
                else:
                    if i == dec[2] and j == dec[3]:
                        s += '*'
                    else:
                        s += '#'
            print(s)
    # def _render(self, mode='human', close=False):
    #     if close:
    #         return
    #
    #     outfile = StringIO() if mode == 'ansi' else sys.stdout
    #
    #     out = self.desc.copy().tolist()
    #     out = [[c.decode('utf-8') for c in line] for line in out]
    #     taxirow, taxicol, passidx, destidx = self.decode(self.s)
    #     def ul(x): return "_" if x == " " else x
    #     if passidx < 4:
    #         out[1+taxirow][2*taxicol+1] = utils.colorize(out[1+taxirow][2*taxicol+1], 'yellow', highlight=True)
    #         pi, pj = self.locs[passidx]
    #         out[1+pi][2*pj+1] = utils.colorize(out[1+pi][2*pj+1], 'blue', bold=True)
    #     else: # passenger in taxi
    #         out[1+taxirow][2*taxicol+1] = utils.colorize(ul(out[1+taxirow][2*taxicol+1]), 'green', highlight=True)
    #
    #     di, dj = self.locs[destidx]
    #     out[1+di][2*dj+1] = utils.colorize(out[1+di][2*dj+1], 'magenta')
    #     outfile.write("\n".join(["".join(row) for row in out])+"\n")
    #     if self.lastaction is not None:
    #         outfile.write("  ({})\n".format(["South", "North", "East", "West", "Pickup", "Dropoff"][self.lastaction]))
    #     else: outfile.write("\n")
    #
    #     # No need to return anything for human
    #     if mode != 'human':
    #         return outfile
