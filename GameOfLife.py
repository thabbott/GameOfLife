"""
Run a PvP version of Conway's Game of Life

Rules:
    - The board is 2MxN grid points
    - Each player specifies an initial arrangement of cells in their
      MxN half of the board
    - The cells evolve for T time steps. On each time step, cells interact
      with their 8 neighboring grid points to...
    - ... die if they have less than 2 neighbors
    - ... survive if they have 2 or 3 neighbors
    - ... die if they have more than 3 neighbors
    - ("Neighbors" include cells belonging to both players)
    - Additionally, a cell is born on all empty grid points with exactly
      3 neighbors. This cells belongs to the player with the majority of 
      the 3 neighbors.
    - If one player's cells go extinct before T time steps have elapsed,
      the other player wins. Otherwise, the player with the most cells 
      after T time steps wins.
    - Tiebreaker (used if players are tied after T time steps, or if both
      players' cells go extent on the same time step): 
      the board gets randomly seeded with one new cell for
      each player and evolves for one time step. If both players have 0 
      cells, the board is reset to its initial configuration before random 
      seeding. This repeats until one
      player has more cells than the other. The random seeds can replace
      cells that are already present but will not overlap with each other.
"""

import os
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import random

class GameOfLife:

    """
    Initialize a game.

    Inputs:
        - red_name (string): name for the red team
        - black_name (string): name for the black team
        - M, N (integer): dimensions of the 2M*N grid
        - T (integer: number of time steps
    """
    def __init__(self, M, N, T):

        self.red_name = ""
        self.black_name = ""
        self.red = np.zeros((N, 2*M), dtype = np.int8)
        self.black = np.zeros((N, 2*M), dtype = np.int8)
        self.red_history = np.nan*np.zeros((T + 1,), dtype = int)
        self.black_history = np.nan*np.zeros((T + 1,), dtype = int)
        self.M = M
        self.N = N
        self.T = T
        self.t = 0
        fig, axes = plt.subplots(nrows = 2, ncols = 1,
                figsize = (7, 8), dpi = 100)
        self.fig = fig
        self.axes = axes
        self.image = axes[0].imshow(self.red - self.black, 
                vmin = -1.5, vmax = 1.5, cmap = "seismic")
        axes[0].yaxis.set_major_locator(plt.NullLocator())
        axes[0].xaxis.set_major_locator(plt.NullLocator())
        self.red_history_plot, = axes[1].plot(
                range(0, self.T+1), self.red_history,
                "r-", alpha=0.75, label = self.red_name)
        self.black_history_plot, = axes[1].plot(
                range(0, self.T+1), self.black_history,
                "b-", alpha=0.75, label = self.red_name)
        axes[1].set_xlim((0, T))
        axes[1].set_xlabel("Round")
        axes[1].set_ylabel("Cells")

    """
    Update the displayed board
    """
    def update_display(self):
        self.axes[0].set_title("%s vs. %s" % 
                (self.red_name, self.black_name))
        self.image.set_data(self.red - self.black)
        self.red_history_plot.set_data(
                range(0, self.T+1), self.red_history)
        self.black_history_plot.set_data(
                range(0, self.T+1), self.black_history)
        yl = self.axes[1].get_ylim()
        dmax = 1.1*max(self.red_history[self.t], 
                self.black_history[self.t])
        if yl[1] < dmax:
            self.axes[1].set_ylim((0, dmax))
        self.axes[1].legend(
                [self.red_history_plot, self.black_history_plot],
                ["%s (%d)" % (self.red_name, self.red_history[self.t]),
                 "%s (%d)" % (self.black_name, self.black_history[self.t])],
                loc = 'upper right',
                frameon = False)
        plt.pause(0.01)

    """
    Save snapshot of displayed board
    """
    def save_display(self):
        match_name = f"{self.red_name}_vs_{self.black_name}"
        dir_name = f"movies/{match_name}"
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        self.fig.savefig(
            f"movies/{match_name}/{str(np.int64(self.t/3)).zfill(4)}.png",
            bbox_inches='tight', dpi=100.
        )
        


    """
    Read from a file to set a player's initial cell configuration
    
    The file must contain M columns and N rows of 0s and 1s
    (other characters will be ignored, grid points will be left
    empty by default if there are less than M*N 0s and 1s, and extra
    0s and 1s will be ignored). The file name is used as the team name

    Inputs:
        - f (string): input file name
        - red (boolean kwarg): True (defult) if reading a file for
          the red player; False if reading a file for the black player
    """
    def read_state_from_file(self, fname, red = True):
        
        arr = np.zeros(self.N*self.M, dtype = np.int8)
        ii = 0
        with open(fname, "r") as f:
            for line in f:
                for ch in line:
                    if ii >= self.M*self.N:
                        continue
                    if ch == "0":
                        arr[ii] = 0
                        ii += 1
                    elif ch == "1":
                        arr[ii] = 1
                        ii += 1
        arr = np.reshape(arr, (self.N, self.M))
        if red:
            self.red[:, :self.M] = arr
            self.red_name = fname.replace("entries/","")
            self.red_history[0] = np.sum(self.red)
        else:
            self.black[:, self.M:] = arr
            self.black_name = fname.replace("entries/","")
            self.black_history[0] = np.sum(self.black)

    """
    Advance the cells by one time step
    """
    def evolve(self):

        kernel = np.ones((3, 3), dtype = np.int8)
        kernel[1,1] = 0
        red_neighbors = signal.convolve2d(self.red, kernel,
                mode = 'same', boundary = 'wrap')
        black_neighbors = signal.convolve2d(self.black, kernel,
                mode = 'same', boundary = 'wrap')
        survival_mask = (
                ((red_neighbors + black_neighbors) == 2) |
                ((red_neighbors + black_neighbors) == 3)
                )
        red_birth_mask = (
                (self.red + self.black == 0) &
                (red_neighbors > black_neighbors) &
                ((red_neighbors + black_neighbors) == 3)
                )
        black_birth_mask = (
                (self.red + self.black == 0) &
                (red_neighbors < black_neighbors) &
                ((red_neighbors + black_neighbors) == 3)
                )
        red_mask = (
                ((self.red > 0) & survival_mask) |
                red_birth_mask
                )
        black_mask = (
                ((self.black > 0) & survival_mask) |
                black_birth_mask
                )
        self.red[:,:] = 0
        self.red[red_mask] = 1
        self.black[:,:] = 0
        self.black[black_mask] = 1
        if self.t < len(self.red_history)-1:
            self.t += 1
            self.red_history[self.t] = np.sum(self.red)
            self.black_history[self.t] = np.sum(self.black)


    """
    Check if red has won
    """
    def red_has_won(self):
        return ((np.sum(self.red) > 0 and np.sum(self.black) == 0) or
                ((self.t >= self.T) and 
                 (np.sum(self.red) > np.sum(self.black))
                ))
    
    """
    Display result
    """
    def display_result(self, code):
        if code == "red":
            self.axes[0].set_title("%s wins!" % self.red_name)
        elif code == "black":
            self.axes[0].set_title("%s wins!" % self.black_name)
        else:
            self.axes[0].set_title("Tiebreaker needed!")
        plt.pause(0.01)

    """ 
    Check if black has won
    """
    def black_has_won(self):
        return ((np.sum(self.black) > 0 and np.sum(self.red) == 0) or
                ((self.t >= self.T) and 
                 (np.sum(self.black) > np.sum(self.red))
                ))

    """
    Check if a tiebreaker is needed
    """
    def tiebreaker_needed(self):
        return ((np.sum(self.black) == 0 and np.sum(self.red) == 0) or
                ((np.sum(self.black) == np.sum(self.red)) and
                 (self.t >= self.T)))


    """
    Seed random cells
    """
    def seed_random_cells(self):
        
        if np.sum(self.red) == 0 and np.sum(self.black) == 0:
            self.read_state_from_file(self.red_name, red = True)
            self.read_state_from_file(self.black_name, red = False)

        ired = 0
        jred = 0
        iblack = 0
        jblack = 0
        while ired == iblack and jred == jblack:
            jred = random.randint(0, 2*self.M-1)
            jblack = random.randint(0, 2*self.M-1)
            ired = random.randint(0, self.N-1)
            iblack = random.randint(0, self.N-1)
        self.red[ired,jred] = 1
        self.black[iblack,jblack] = 1
