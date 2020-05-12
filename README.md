# Whizkey Game of Life tournament

See GameOfLife.py for rules!

This code uses a few Python packages. To install them, download and install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) (or use your conda installation if you have one), create a new conda environment by running
```shell
conda create --name gameoflife python=3.7
```
To install the packages needed to run ``play_game.py`` and ``draw_input_matplotlib.py``, run
```shell
conda install numpy scipy matplotlib
```
Running ``draw_input.py`` also requires OpenCV, which can be installed by running
```shell
conda install -c conda-forge opencv
```

To play a game, run
```shell
python play_game.py
```
This game reads initial cell configurations from the ``Ronaldo`` and ``Messi`` files and then allows them to evolve for 1000 time steps. 

You can create your own input files by running
```shell
python draw_input_matplotlib.py
```
or
```shell
python draw_input.py
```
and use them in the example game by replacing "Ronaldo" and/or "Messi" on lines 3 and/or 4 of ``play_game.py``. All you have to do to enter the tournament is send one (or more!) input file(s) to Tristan and/or Santi by May 25. (Name the file whatever you want your team name to be.) The only limitation is that your input file **cannot have more than ??? active cells** (number TBD).
