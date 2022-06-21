# infected-cell-dash-compare

## Overall Goal of this Project:
To run a dash app using sample CRISPR screen data comparison

## Dependencies:
* Make sure to install conda
* The Visual Studio Code Python extension installed

## To run this project:
1. `cd infected-cell-dash-compare`
2. `conda env create --file environment.yml` to create a conda environment with the required dependencies. *If you already have the environment installed you can skip this step.*
3. Open Visual Studio Code in the current directory with `code .`
4. To point VSCode to the right conda environment, select the `src/app.py` file.
5. Wait a few seconds for VSCode's Python extension to get started up.
6. In the bottom right corner, there should be a button that says "Select Python Interpreter". Click it and it should bring up a menu in the top middle. Select the environment that says `Python 3.XX.X ('dash-ds-infected-cell')`.
7. You're ready! Note that some Python files may require an argument to the path where the data is. For example, to run `single-app.py`, the command would be like `python single-app.py PATH_TO_FOLDER/output_072321/`.
