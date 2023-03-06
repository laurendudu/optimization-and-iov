import matplotlib.pyplot as plt
import pandas as pd

from utils.nsgaii import chromosome_to_network


def plot_network(network: list, tasks: list):
    # make the plot bigger
    plt.figure(figsize=(6, 6))

    # add a grid at the background
    plt.grid(color="white", linestyle="-", linewidth=1)

    # set the background color
    plt.gca().set_facecolor("#d9ead3")

    # label the axes
    plt.xlabel("X")
    plt.ylabel("Y")

    # plot the tasks
    for task in tasks:
        plt.scatter(task.X, task.Y, color="purple", s=10)

    # plot the network
    for rsu in network:
        if rsu.ES == "AP":
            plt.text(rsu.X, rsu.Y, rsu.ES, fontsize=10)
            plt.scatter(rsu.X, rsu.Y, color="orange", s=50)
        else:
            plt.text(rsu.X, rsu.Y, "ES", fontsize=10)
            plt.scatter(rsu.X, rsu.Y, color="green", s=50)

    # title the plot
    plt.title("Representation of the network")

    return plt.show()


def plot_solution(solution, tasks: list):

    network = chromosome_to_network(solution.chromosome)

    # make the plot bigger
    plt.figure(figsize=(6, 6))

    # add a grid at the background
    plt.grid(color="white", linestyle="-", linewidth=1)

    # set the background color
    plt.gca().set_facecolor("#d9ead3")

    # label the axes
    plt.xlabel("X")
    plt.ylabel("Y")

    # plot the tasks
    for task in tasks:
        plt.scatter(task.X, task.Y, color="purple", s=10)

    # plot the network
    for rsu in network:
        if rsu.ES == "AP":
            plt.text(rsu.X, rsu.Y, rsu.ES, fontsize=10)
            plt.scatter(rsu.X, rsu.Y, color="orange", s=50)
        else:
            plt.text(rsu.X, rsu.Y, "ES", fontsize=10)
            plt.scatter(rsu.X, rsu.Y, color="green", s=50)

    # title the plot
    plt.title(f"Representation of the network, fitness={solution.fitness}")

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
