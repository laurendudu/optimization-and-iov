import random

from .offloading import task_offloading
from .objects import Task, RSU, ES


class Individual(object):
    """Individual of the NSGA-II algorithm.

    Attributes:
        chromosome (list): chromosome of the individual.
        fitness (list): fitness of the individual.
    """

    global_individual = []

    def __init__(self, network):

        # create the chromosome
        self.chromosome = network_to_chromosome(network)

        # compute the fitness
        self.fitness = fitness(network)

        self.rank = None
        self.__class__.global_individual.append(self)
        self.ID = len(self.__class__.global_individual)
        self.domination_list = []
        self.crowding_distance = None

    def __str__(self) -> str:
        """Returns a string representation of the individual.

        Returns:
            str: string representation of the individual.
        """
        for i in range(len(self.chromosome)):
            if i == 0:
                string = f"{self.chromosome[i]}"
            else:
                string += f", {self.chromosome[i]}"
        return string

    # dominates method
    def dominates(self, other):
        """Checks if the individual dominates another individual.

        Args:
            other (Individual): individual to compare to.

        Returns:
            bool: True if the individual dominates the other individual, False otherwise.
        """
        # check if the individual dominates the other individual
        if all(
            self.fitness[i] <= other.fitness[i] for i in range(len(self.fitness))
        ) and any(self.fitness[i] < other.fitness[i] for i in range(len(self.fitness))):
            return True
        return False


def network_to_chromosome(network):
    # get the list of RSU from the chromosome
    rsus = [rsu for rsu in network]
    # get the list of ES from the chromosome
    es_rsus = [rsu for rsu in network if rsu.ES != "AP"]

    # sort the first list of RSU by RSU ID
    rsus.sort(key=lambda x: x.ID)
    # sort the second list of RSU by ES ID
    es_rsus.sort(key=lambda x: x.ES.ID)

    # get the coordinates of each RSU in rsus + es_rsus
    rsu_coordinates = [(rsu.ID, rsu.X, rsu.Y) for rsu in rsus]
    es_rsu_link = [(rsu.ES.ID, rsu.ID) for rsu in es_rsus]

    return rsu_coordinates + es_rsu_link


def chromosome_to_network(chromosome):
    """Converts a chromosome to a network.

    Args:
        rsu_bank (list): list of RSU.
        es_bank (list): list of ES.
        chromosome (list): chromosome of the individual.

    Returns:
        list: list of RSU.
    """
    # get the instances of the RSU and ES classes
    rsu_bank = RSU.global_rsu
    es_bank = ES.global_es

    number_of_rsus = len(rsu_bank)

    # get the list of RSU from the chromosome
    chromosome_rsu_info = chromosome[:number_of_rsus]
    # get the list of ES from the chromosome
    chromosome_es_info = chromosome[number_of_rsus:]

    # update the coordinates of the RSUs
    # if the first element of the tuple is the same as the RSU ID, update the coordinates
    for rsu in rsu_bank:
        for gene in chromosome_rsu_info:
            if rsu.ID == gene[0]:
                rsu.X = gene[1]
                rsu.Y = gene[2]

    # set all the RSUs to be APs
    for rsu in rsu_bank:
        rsu.ES = "AP"

    # update the ES of the RSUs
    # if the first element of the tuple is the same as the ES ID, update the ES
    for rsu in rsu_bank:
        for gene in chromosome_es_info:
            if rsu.ID == gene[1]:
                for es in es_bank:
                    if es.ID == gene[0]:
                        rsu.ES = es

    return rsu_bank


def fitness(network):
    # get all instances of the Task class
    tasks_bank = Task.global_task

    # reset the history of the tasks and RSUs
    fresh_network, fresh_tasks = reset_history(network, tasks_bank)

    final_tasks = task_offloading(network=fresh_network, tasks_bank=fresh_tasks)

    # get the max COMPUTATION_HISTORY of all the tasks
    max_computation = max(task.COMPUTATION_HISTORY for task in final_tasks)
    # get the max MIGRATION_HISTORY of all the tasks
    max_migration = max(task.MIGRATION_HISTORY for task in final_tasks)

    return max_computation, max_migration


def reset_history(network, tasks_bank):
    """Resets the history of the tasks.

    Args:
        network (list): list of RSU.
        tasks_bank (list): list of Task.
    """
    # reset the tasks
    for task in tasks_bank:
        task.COMPUTATION_HISTORY = 0
        task.MIGRATION_HISTORY = 0
        task.MIGRATION_TIME = 0
        task.COMPLETED = False
        task.RSU_HISTORY = []

    # reset the RSUs
    for rsu in network:
        rsu.STATE = "IDLE"
        rsu.END_TIME = None

    return network, tasks_bank


def crossing(parent_1: Individual, parent_2: Individual) -> tuple:
    """Crosses two individuals.

    Args:
        parent_1 (Individual): first parent.
        parent_2 (Individual): second parent.

    Returns:
        Individual: child.
    """
    # get the chromosome of the parents
    chromosome_1 = parent_1.chromosome.copy()
    chromosome_2 = parent_2.chromosome.copy()

    # get the number of genes of the chromosomes
    number_of_genes = len(chromosome_1)

    # get the crossover point
    crossover_point = random.randint(0, number_of_genes - 1)

    # create child chromosome 1
    child_chromosome_1 = chromosome_1[:crossover_point] + chromosome_2[crossover_point:]
    # create child chromosome 2
    child_chromosome_2 = chromosome_2[:crossover_point] + chromosome_1[crossover_point:]

    # create a network and Individual from the child chromosome 1
    child_network_1 = chromosome_to_network(child_chromosome_1)
    child_1 = Individual(child_network_1)

    # create a network and Individual from the child chromosome 2
    child_network_2 = chromosome_to_network(child_chromosome_2)
    child_2 = Individual(child_network_2)

    return child_1, child_2


def mutation(individual: Individual) -> Individual:
    # get the chromosome of the individual
    chromosome = individual.chromosome.copy()

    # get the number of genes of the chromosome
    number_of_genes = len(chromosome)

    # get the mutation point
    mutation_point = random.randint(0, number_of_genes - 1)

    # get the gene to be mutated
    gene = chromosome[mutation_point]

    # get the length of the gene
    gene_length = len(gene)

    # if the gene is a tuple of 3 elements, it is a RSU
    if gene_length == 3:
        # create new coordinates for the RSU
        new_X = random.randint(0, 100)
        new_Y = random.randint(0, 100)

        # replace the old coordinates with the new ones
        chromosome[mutation_point] = (gene[0], new_X, new_Y)

    # if the gene is a tuple of 2 elements, it is an ES
    elif gene_length == 2:
        # get the list of RSU IDs
        rsu_ids = [rsu.ID.copy() for rsu in RSU.global_rsu]

        # get the list of RSU IDs that are already connected to an ES
        connected_rsu_ids = [gene[1] for gene in chromosome if len(gene) == 2]

        # choose a random RSU ID that is not already connected to an ES
        new_rsu_id = random.choice(list(set(rsu_ids) - set(connected_rsu_ids)))

        # replace the old RSU ID with the new one
        chromosome[mutation_point] = (gene[0], new_rsu_id)

    network = chromosome_to_network(chromosome)

    return Individual(network)


def non_dominated_sorting(population):
    """Sorts the population by non-dominated sorting.

    Args:
        population (list): list of individuals.

    Returns:
        list: list of individuals.
    """
    # reset the ranks and domination lists of the individuals
    for individual in population:
        individual.rank = None
        individual.domination_list = []

    # Initialize the fronts
    fronts = [[]]
    # Initialize the number of individuals that dominate each individual
    domination_count = [0] * len(population)

    for i, individual_1 in enumerate(population):
        for j, individual_2 in enumerate(population):
            # if individual_1 dominates individual_2
            if individual_1.dominates(individual_2):
                # add individual_2 to the domination list of individual_1
                individual_1.domination_list.append(individual_2)
            # if individual_2 dominates individual_1
            elif individual_2.dominates(individual_1):
                # increase the domination count of individual_2
                domination_count[j] += 1

        # if individual_1 is not dominated by any other individual
        if domination_count[i] == 0:
            # add individual_1 to the first front
            fronts[0].append(individual_1)
            # set the rank of individual_1 to 1
            individual_1.rank = 1

    # Calculate the rank of each individual
    i = 0
    while fronts[i]:
        next_front = []
        for individual in fronts[i]:
            for dominated_individual in individual.domination_list:
                # decrease the domination count of dominated_individual
                domination_count[population.index(dominated_individual)] -= 1
                # if dominated_individual is not dominated by any other individual
                if domination_count[population.index(dominated_individual)] == 0:
                    # add dominated_individual to the next front
                    next_front.append(dominated_individual)
                    # set the rank of dominated_individual to i + 2
                    dominated_individual.rank = i + 2
        i += 1
        fronts.append(next_front)

    return fronts[:-1]


def crowding_distance(fronts):
    """Calculates the crowding distance of each individual in the population.

    Args:
        fronts (list): list of fronts.

    Returns:
        list: list of fronts with updated crowding distances.
    """

    # initialize the crowding distance of each individual to 0
    for front in fronts:
        for individual in front:
            individual.crowding_distance = 0

    # for each objective
    for objective in range(2):
        # for each front
        for front in fronts:
            # sort the individuals in the front by the objective
            front.sort(key=lambda x: x.fitness[objective])

            # set the crowding distance of the first and last individual to infinity
            front[0].crowding_distance = float("inf")
            front[-1].crowding_distance = float("inf")

            # calculate the crowding distance of the other individuals
            for i in range(1, len(front) - 1):
                front[i].crowding_distance += (
                    front[i + 1].fitness[objective] - front[i - 1].fitness[objective]
                ) / (front[-1].fitness[objective] - front[0].fitness[objective])

    return fronts


def tournament_selection(population, tournament_size):
    """Selects an individual from the population using tournament selection.

    Args:
        population (list): list of individuals.
        tournament_size (int): size of the tournament.

    Returns:
        Individual: the selected individual.
    """
    # choose tournament_size individuals randomly from the population
    tournament = random.sample(population, tournament_size)

    best_individual = tournament[0]

    tournament = crowding_distance(tournament)

    # find the best individual in the tournament
    for individual in tournament:
        if individual.dominates(best_individual):
            best_individual = individual
        elif not best_individual.dominates(individual):
            if individual.crowding_distance > best_individual.crowding_distance:
                best_individual = individual

    return best_individual
