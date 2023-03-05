import pandas as pd
import numpy as np


class RSU:
    """Represents an RSU."""

    global_rsu = []

    def __init__(
        self,
        ID,
        X,
        Y,
        DTR,
    ):
        self.ID = ID
        self.X = X
        self.Y = Y
        self.DTR = DTR
        self.STATE = "IDLE"
        self.END_TIME = None
        self.ES = None
        self.__class__.global_rsu.append(self)


class ES:
    """Represents an ES."""

    global_es = []

    def __init__(
        self,
        ID,
        VM_NB,
        VM_CP,
    ):
        self.ID = ID
        self.VM_NB = VM_NB
        self.VM_CP = VM_CP
        self.__class__.global_es.append(self)


class Task:
    """Represents a task."""

    global_task = []

    def __init__(
        self,
        ID,
        LENGTH,
        FILE_SIZE,
        TYPE,
        X,
        Y,
    ):
        self.ID = ID
        self.LENGTH = LENGTH
        self.FILE_SIZE = FILE_SIZE
        self.TYPE = TYPE
        self.X = X
        self.Y = Y
        self.COMPLETED = False
        self.MIGRATION_HISTORY = 0
        self.COMPUTATION_HISTORY = 0
        self.MIGRATION_TIME = 0
        self.RSU_HISTORY = []
        self.__class__.global_task.append(self)


def populate_tasks(data: pd.DataFrame) -> list:
    """Populates the task list with the tasks from the data file.

    Args:
        data (pd.DataFrame): dataframe containing the tasks.
    """
    tasks = []
    for i in range(len(data)):
        task = Task(
            ID=data["ID"][i],
            LENGTH=data["LENGTH"][i],
            FILE_SIZE=data["FILE_SIZE"][i],
            TYPE=data["TYPE"][i],
            X=data["X"][i],
            Y=data["Y"][i],
        )
        tasks.append(task)

    return tasks


def populate_rsus(data: pd.DataFrame) -> list:
    """Populates the RSU list with the RSUs from the data file.

    Args:
        data (pd.DataFrame): dataframe containing the RSUs.
    """
    rsus = []
    for i in range(len(data)):
        rsu = RSU(
            ID=data["ID"][i],
            X=data["X"][i],
            Y=data["Y"][i],
            DTR=data["DTR"][i],
        )
        rsus.append(rsu)

    return rsus


def populate_ess(data: pd.DataFrame) -> list:
    """Populates the ES list with the ESs from the data file.

    Args:
        data (pd.DataFrame): dataframe containing the ESs.
    """
    ess = []
    for i in range(len(data)):
        es = ES(
            ID=data["ID"][i],
            VM_NB=data["VM_NB"][i],
            VM_CP=data["VM_CP"][i],
        )
        ess.append(es)

    return ess


def get_network(rsu: list, es: list) -> list:
    """Generates a network of RSUs and ESs from the RSU and ES lists.

    Args:
        rsu (list): list of RSUs.
        es (list): list of ESs.

    Returns:
        list: list of RSUs with ESs assigned to them.
    """
    # choose a random number of RSUs M
    M = np.random.randint(2, len(rsu))
    # choose a random number of ESs W, with W < M
    W = np.random.randint(1, M)

    # choose M RSUs from the RSU bank
    rsu_list = np.random.choice(rsu, M, replace=False)
    # choose W ESs from the ES bank
    es_list = np.random.choice(es, W, replace=False)

    # shuffle the RSU list and the ES list
    np.random.shuffle(rsu_list)
    np.random.shuffle(es_list)

    # for each es, choose an rsu to connect to
    for i, es in enumerate(es_list):
        rsu_list[i].ES = es

    # for each rsu, if ES is None, set it to 'AP'
    for rsu in rsu_list:
        if rsu.ES is None:
            rsu.ES = "AP"

    # shuffle the RSU list again
    np.random.shuffle(rsu_list)

    return rsu_list


def get_random_network(rsu_list: list, es_list: list) -> list:
    """Generates a random network of RSUs and ESs from the RSU and ES lists.

    Args:
        rsu_list (list): list of RSUs.
        es_list (list): list of ESs.

    Returns:
        list: list of RSUs with ESs assigned to them, all of them with random coordinates.
    """
    # shuffle the RSU list and the ES list
    np.random.shuffle(rsu_list)
    np.random.shuffle(es_list)

    # for each RSU, generate random coordinates
    for rsu in rsu_list:
        rsu.X = np.random.randint(0, 100)
        rsu.Y = np.random.randint(0, 100)

    # reset the ES of the RSUs
    for rsu in rsu_list:
        rsu.ES = None

    # for each es, choose an rsu to connect to
    for i, es in enumerate(es_list):
        rsu_list[i].ES = es

    # for each rsu, if ES is None, set it to 'AP'
    for rsu in rsu_list:
        if rsu.ES is None:
            rsu.ES = "AP"

    return rsu_list
