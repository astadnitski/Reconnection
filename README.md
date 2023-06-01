# Reconnection research

Running this analysis requires the following:

- Timestep `vtk` files saved to subdirectory `xolinesVTK/`

- Timestep stagnation line coordinate `csv` files saved to subdirectory `staglinesCSV/`

- Timestep vertical lines (for stack plot) saved to `vlinesCSV/`

## 1. Generating individual plots

- Run `SaveXO.py` with PvPython

    - Output is saved to subdirectory `xolinesCSV/`

- Run `SelectX.py` with Python3, or submit job `selectx.slurm`

    - X-line coordinates and line data saved to `xlinesCSV/`

    - Plots saved to `xplots/`

## 2. Generating stack plot in time

The stack plot requires files for every timestep to be present in the `xolinesCSV/` subdirectory.

- Run `PlotAllTime.py` with Python3

    - Plot is saved as `AllPlot.png`

## 3. Computing integrals

The stack plot requires files for every timestep to be present in the `xlinesCSV/` subdirectory.

- Run `Integration.py` with Python3

    - By toggling `lines = True/False`, plot is saved alternately as either

        - `IntegralsLinePlot.png`

        - `IntegralsScatterPlot.png`
    
    - Integrated values are saved as `Integrals.csv`

