# Task offloading and edge computing: modeling a system of connected cars

This repository contains code for generating artificial data, running a task offloading process, and applying the NSGA-ii algorithm on an IoV system.

For a set of fixed tasks, the goal is to minimize their migation time and their computation time along a network of Road Side Units (RSU). These RSU are either edge servers (ES), or access points (AP).

To understand more about how the mathematical theory works, please refer to this [document](https://laurendu.notion.site/Task-offloading-et-edge-computing-mod-lisation-d-un-syst-me-de-voitures-connect-es-et-autonomes-fe6caa8eaa514edcb86c582c6db85d99). 

## How does the code work?
All the code is commented, what is important is to run the notebooks in the correct order.

Firstly, you must run the `datagen.ipynb` notebook to generate artificial data. Once that is done, you can run the `offloading.ipynb` notebook. That one runs the offloading process once, for a network. You can understand clearly how the process works. 

The `nsgaii.ipynb` notebook contains the nsga2 algorithm function, which looks for a set of Pareto solutions, minimizing the max of both objective functions. It also tests multiple variables such as population size, amount of generations, etc..


The `plots.ipynb` notebook displays useful plots to understand the problem better, and also visualizes the pareto solutions for the best conditions found.

## The `utils` folder
This folder contains _all_ functions used in the notebooks. The NSGA-II algorithm is coded by hand, as well as the task offloading process. 
