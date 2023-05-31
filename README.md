# Reconnection research

Running this analysis requires the following:

- Timestep `vtk` files saved to subdirectory `xolinesVTK/`

- Timestep stagnation line coordinate `csv` files saved to subdirectory `staglinesCSV/`

- Timestep vertical lines (for stack plot) saved to `vlinesCSV/`

## Generating individual plots

- Run `SaveXO.py` with PvPython

    - Output is saved to subdirectory `xolinesCSV/`

- Run `SelectX.py` with Python3, or submit job `selectx.slurm`

    - X-line coordinates and line data saved to `xlinesCSV/`

    - Plots saved to `xplots/`

## Generating stack plot in time

The stack plot requires files for every timestep to be present in the `xolinesCSV/` subdirectory.

- Run `PlotAllTime.py` with Python3

    - Plot is saved as `AllPlot.png`

## Computing integrals