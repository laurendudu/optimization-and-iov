import matplotlib.pyplot as plt
import pandas as pd


def plot_network(network: list, tasks: list):
    # make the plot bigger
    plt.figure(figsize=(6, 6))

    # make the background light green
    plt.gca().set_facecolor("lightgreen")

    # add a grid at the background
    plt.grid(color="white", linestyle="-", linewidth=1)

    # label the axes
    plt.xlabel("X")
    plt.ylabel("Y")

    # plot the tasks
    for task in tasks:
        plt.scatter(task.x, task.y, color="purple", s=10)

    # plot the network
    for rsu in network:
        plt.scatter(rsu.x, rsu.y, color="orange", s=20)
        if rsu.ES == "AP":
            plt.text(rsu.x, rsu.y, rsu.ES, fontsize=10)
        else:
            plt.text(rsu.x, rsu.y, "ES", fontsize=10)

    # title the plot
    plt.title("Representation of the network")

    return plt.show()


def plot_pareto(
    population,
    POPULATION_SIZE,
    MAX_GENERATIONS,
    TOURNAMENT_SIZE,
    CROSSOVER_PROBABILITY,
    MUTATION_PROBABILITY,
):
    # make the plot bigger
    plt.figure(figsize=(5, 5))

    # plot the fitness values of the final population
    # change the color for each rank value
    for individual in population:
        if individual.rank != 1:
            plt.scatter(individual.fitness[0], individual.fitness[1], color="orange")

    for individual in population:
        if individual.rank == 1:
            plt.scatter(individual.fitness[0], individual.fitness[1], color="green")

    # label the axes
    plt.xlabel("Max Computation Time")
    plt.ylabel("Max Migration Time")

    # title the plot
    plt.title(
        f"Pareto front with:\nPOPULATION={POPULATION_SIZE}, GENERATIONS={MAX_GENERATIONS}, TOURNAMENT={TOURNAMENT_SIZE}\nCROSSOVER={CROSSOVER_PROBABILITY}, MUTATION={MUTATION_PROBABILITY}"
    )

    # show the plot
    return plt.show()
