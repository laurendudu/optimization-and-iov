import math


def migration_time(file_size: int, distance: float, dtr: int) -> float:
    """Computes the migration of a task between a AP RSU and an ES.

    Args:
        file_size (int): file size of the task in megabytes.
        distance (float): distance between the RSUs in meters.
        dtr (int): data transfer rate in megabits per second.

    Returns:
        float: migration of the task in seconds.
    """

    return (file_size / dtr) * distance


def computation_time(task_length: int, vm_nb: int, vm_cpu: int) -> float:
    """Computes the computation time of a task.

    Args:
        task_length (int): length of the task in MI
        vm_nb (int): number of VMs in the ES.
        vm_cpu (int): CPU capacity of a VM in MIPS.

    """
    return task_length / (vm_nb * vm_cpu)


def data_transfer_time(file_size: int, dtr: int) -> float:
    """Computes the data transfer time of a task.

    Args:
        file_size (int): file size of the task in megabytes.
        dtr (int): data transfer rate in megabits per second.

    Returns:
        float: data transfer time of the task in seconds.
    """
    return file_size / dtr


def get_closest_rsu(rsu_list: dict, x: int, y: int) -> dict:
    """Returns the index of the closest RSU to a given point.

    Args:
        rsu_list (dict): list of RSUs.
        x (int): x coordinate of the point.
        y (int): y coordinate of the point.

    Returns:
        int: index of the closest RSU.
    """
    min_distance = math.inf
    min_index = -1
    for i in rsu_list.keys():
        distance = math.sqrt(
            (rsu_list[i]["RSU_X"] - x) ** 2 + (rsu_list[i]["RSU_Y"] - y) ** 2
        )
        if distance < min_distance and distance != 0:
            min_distance = distance
            min_index = i
    return min_index


def is_server_free(server: dict) -> bool:
    """Checks if a server is free.

    Args:
        server (dict): server to check.

    Returns:
        bool: True if the server is free, False otherwise.
    """
    return server["RSU_STATE"] == "IDLE"


def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def compatible(rsu, task) -> bool:
    """Checks if a task is compatible with a RSU.

    Args:
        rsu (dict): RSU to check.
        task (dict): task to check.

    Returns:
        bool: True if the task is compatible with the RSU, False otherwise.
    """
    if rsu["ES_ID"] == "AP" and task["TYPE"] == "DATA TRANSFER":
        return True
    elif rsu["ES_ID"] != "AP" and task["TYPE"] == "COMPUTATION":
        return True
    else:
        return False
