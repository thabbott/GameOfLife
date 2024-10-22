# ESS Fall 2024 Half-Baked Game of Life tournament

Hosted by Henri Drake ([@hdrake](https://github.com/hdrake)) and Isba Keshwani ([@ikeshwani](https://github.com/ikeshwani))

![Example match of the Adversarial Game of Life](movies/Messi_vs_Mothership/Messi_vs_Mothership.gif)

See ``GameOfLife.py`` for rules! Learn more about the diverse lifeforms that populate Conway's Game of Life from https://www.conwaylife.com/wiki.

### Setting up the Python environment
This code uses a few Python packages. To install them, first download and install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) (or use your conda installation if you have one), and then either:

1. Create a pre-packaged conda environment with:
```shell
conda env create -f environment.yml
```
or 
2. Create a new conda environment manually by running:
```shell
conda create --name gameoflife python=3.12
```
If creating the environment manually, install the packages needed to run ``play_game.py`` and ``draw_input_matplotlib.py`` by running
```shell
conda install -c conda-forge numpy scipy matplotlib
```

### Playing an adversarial match of Conway's Game of Life
To play a game, run
```shell
python play_game.py
```
By default, this game reads initial cell configurations from the ``BlockTest`` and ``Henri-Drake-Skrrrrt`` files in the ``entries/`` folder and then allows them to evolve for 1000 time steps.

To play a game with other inputs files in the ``entries/`` folder, simply pass the two filenames as arguments to ``play_game.py``:
```shell
python play_game.py [File 1] [File 2]
```

### Entering the ESS Half-Baked "Competitive Game of Life" Tournament on November 8th 2024
To enter the tournament, please create a Game of Life file named `[FirstName]-[LastName]-[StrategyName]` (see instructions below) and submit it to us using one of the following methods by 11:59 PM on November 7th:
1. Create a Pull Request that adds your entry (or multiple entries) to the `entries/` directory of this repository on Github.
2. Send one (or more!) input file(s) to Henri Drake (hfdrake@uci.edu)

### Creating custom inputs files
You can create your own input files by running
```shell
python draw_input_matplotlib.py
```
and clicking on cells to toggle cells between being inactive (white) or active (black).

![Example creation of two configurations and a match between them!](movies/example_small.gif)

### Placing pre-defined patterns
In ```draw_input_matplotlib.py```, we have added the ability to load pre-existing Game of Life patterns in the conventional [Run Length Encoded (RLE) format](https://www.conwaylife.com/wiki/Run_Length_Encoded). We have placed some common example patterns in ``patterns/``. To load in a pattern, simply run ``python draw_input_matplotlib.py`` and instead of clicking to toggle a single cell, press the `A` key (for "**A**dd pattern"). Type the name of the desired pattern (e.g. *glider*) in the terminal prompt and hit enter. When you return to the figure, you will see the outline of the pattern under your cursor and can place it on the grid by clicking. When you are done placing copies of the pattern, simply toggle the "Add pattern" mode off by pressing the `T` key (for "**T**oggle add pattern").

The following transformations can be applied to a pattern by appending a pattern name with a period and a series of transformations, each separated by an underscore:
- `rx`: reflection in x
- `ry`: reflection in y
- `r90`: counter-clockwise rotation by 90°
- `r180`: counter-clockwise rotation by 180°

Other transformations, such as rotation by 270° degrees, can be accomplished by chaining the above transformations (e.g. `glider.r90_r180` will rotate a glider first 90° and then another 180° for a total of 270°.
