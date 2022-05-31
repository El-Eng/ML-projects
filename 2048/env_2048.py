import re
import numpy as np
import gym
from gym import Env, spaces, utils
import pygame
from typing import Optional
from io import StringIO
from contextlib import closing

# env = BlockDoubleEnv()
# env.reset()
# action = env.action_space.sample()
# observation, reward, done, info = env.step(action)
# env.render(mode = "ansi")

class BlockDoubleEnv(gym.Env):
    metadata = {"render_modes": ["human", "ansi"], "render_fps": 4}

    def __init__(self, render_mode: Optional[str] = None, size: int = 4):
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        render_mode = 'ansi'
        self.size = size  # The size of the square grid
        self.window_size = 512  # The size of the PyGame window

        # Observations are dictionaries with the agent's and the target's location.
        # box
        self.observation_space = spaces.Box(low= 0, high= 2048, shape=(16, ), dtype=int)

        # We have 4 actions, corresponding to "right", "up", "left", "down", "right"
        self.action_space = spaces.Discrete(4)

        """
        If human-rendering is used, `self.window` will be a reference
        to the window that we draw to. `self.clock` will be a clock that is used
        to ensure that the environment is rendered at the correct framerate in
        human-mode. They will remain `None` until human-mode is used for the
        first time.
        """
        # if render_mode == "human":
        #     import pygame  # import here to avoid pygame dependency with no render

        #     pygame.init()
        #     pygame.display.init()
        #     self.window = pygame.display.set_mode((self.window_size, self.window_size))
        #     self.clock = pygame.time.Clock()

        self.window = None
        self.clock = None
        #self.renderer = Renderer(render_mode, self._render_frame)
    def _get_obs(self):
        return  self._boardstate
    def _get_info(self):
        return {"score": np.amax(self._boardstate)}

    def reset(self, seed=None, return_info=False, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        # Set board to reset with random tile a 2
        boardstart = np.zeros((self.size,self.size))
        boardstart[self.np_random.integers(0, self.size-1)][self.np_random.integers(0, self.size-1)] = 2
        self._boardstate = boardstart

        observation = self._get_obs().flatten()
        info = self._get_info()
        return (observation, info) if return_info else observation

    def step(self, action, done=False, loose=False):
        point = 0
        info = self._get_info()
        # 0,1,2,3 => right,down,left,up (left right odd)
        direction = action
        # Logic for shiftng board left and right
        flip = np.rot90(self._boardstate, direction)
        shift = np.zeros((self.size,self.size))
        # Shifts left to right
        for key, row in enumerate(flip):
            row = row[row != 0]
            x = len(row)-1
            #print(row)
            while 0 < x:
                if row[x] == row[x-1]:
                    row[x] = row[x]*2
                    row[x-1] = 0
                    row = row[row != 0]
                    #print(row)
                    x-=2
                else:
                    x -= 1
            shift[key] = np.pad(row,(self.size - len(row), 0), 'constant')
            #print(shift[key])
        result = np.rot90(shift, 4-direction)

        if np.all(result):
            lost = True
            for row in result:
                for x in range(len(row)-1):
                    if row[x] == row[x+1]:
                        lost = False
            for row in np.rot90(result, 1):
                for x in range(len(row)-1):
                    if row[x] == row[x+1]:
                        lost = False
            if lost:
                done = True
        
        if np.array_equal(self._boardstate, result):
            done=True
        else:
            # add in new number
            zeros = np.argwhere(result == 0) # Indices where board == 0
            indices = np.ravel_multi_index([zeros[:, 0], zeros[:, 1]], result.shape) # Linear indices
            ind = np.random.choice(indices) # Randomly select your index to replace
            result[np.unravel_index(ind, result.shape)] = np.random.choice(a=['2', '4'], p=['0.9', '0.1']) # Perform the replacement

            self._boardstate = result
        
        # if larger tile number than before grant a point
        if self._boardstate.max() > info['score']:
            point = 0.1

        # An episode is done if the max tile is 2048
        reward = point

        if self._boardstate.max() >= 2048:
            done=True 
            reward = 100 

        observation = self._get_obs().flatten()
        info = self._get_info()

        return observation, reward, done, info

    def render(self, mode="ansi"):
        desc = self._boardstate.tolist()
        if mode == "ansi":
            return self._render_text(desc)
        # else:
        #     return self._render_gui(desc, mode)

    def _render_text(self, desc):
        outfile = StringIO()
        # desc=["SFFF", "FHFH", "FFFH", "HFFG"].
        #desc = [[c for c in line] for line in desc]
        #outfile.write("\n".join("".join(str(line)) for line in ) + "\n")
        outfile.write("\n".join("".join(str(line)) for line in desc) + "\n")

        with closing(outfile):
            return outfile.getvalue()

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
           
# from gym.envs.registration import register
# import gym_examples

# register(
#     id='gym_examples/BlockDouble-v1',
#     entry_point='gym_examples.envs:GridWorldEnv',
#     max_episode_steps=300,
# )
# env = gym.make('gym_examples/BlockDouble-v1')


# env.reset()
# action = env.action_space.sample()
# observation, reward, done, info = env.step(action)
# env.render(mode = "ansi")

# for _ in range(1000):
#     action = env.action_space.sample()
#     observation, reward, done, info = env.step(action)
#     env.render(mode = "ansi")
#     if done:
#         observation, info = env.reset(return_info=True)
# env.close()
