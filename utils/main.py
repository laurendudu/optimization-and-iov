import math
from .objects import RSU, Task


def get_closest_rsu(rsu_list: list, object, exclude_list: list) -> RSU:
    """
    Returns the closest RSU to an object.

    Args:
        rsu_list (list): list of RSUs.
        object (object): object to which the closest RSU is to be found.
        exclude_list (list): list of RSUs to be excluded from the search.

    Returns:
        RSU: closest RSU to the object.
    """
    min_distance = math.inf
    min_rsu = None

    for rsu in rsu_list:
        distance = math.sqrt((rsu.X - object.X) ** 2 + (rsu.Y - object.Y) ** 2)
        if distance < min_distance and rsu not in exclude_list:
            min_distance = distance
            min_rsu = rsu

    return min_rsu


def is_server_free(rsu: RSU) -> bool:
    """Checks if an RSU is free.

    Args:
        rsu (RSU): RSU to be checked.

    Returns:
        bool: True if the RSU is free, False otherwise.
    """
    return rsu.STATE == "IDLE"


def compatible(rsu: RSU, task: Task) -> bool:
    """Checks if an RSU is compatible with a task.

    Args:
        rsu (RSU): RSU to be checked.
        task (Task): task to be checked.

    Returns:
        bool: True if the RSU is compatible with the task, False otherwise.
    """
    if rsu.ES == "AP" and task.TYPE == "DATA TRANSFER":
        return True
    elif rsu.ES != "AP" and task.TYPE == "COMPUTATION":
        return True
    else:
        return False


def computation_time(task_length: int, vm_nb: int, vm_cpu: int) -> float:
    """Computes the computation time of a task.

    Args:
        task_length (int): length of the task in MI
        vm_nb (int): number of VMs in the ES.
        vm_cpu (int): CPU capacity of a VM in MIPS.

    """
    return math.ceil(task_length / (vm_nb * vm_cpu))


def migration_time(file_size: int, distance: float, dtr: int) -> float:
    """Computes the migration of a task between a AP RSU and an ES.

    Args:
        file_size (int): file size of the task in megabytes.
        distance (float): distance between the RSUs in meters.
        dtr (int): data transfer rate in megabits per second.

    Returns:
        float: migration of the task in seconds.
    """

    return math.ceil((file_size / dtr) * distance)


def data_transfer_time(file_size: int, dtr: int) -> float:
    """Computes the data transfer time of a task.

    Args:
        file_size (int): file size of the task in megabytes.
        dtr (int): data transfer rate in megabits per second.

    Returns:
        float: data transfer time of the task in seconds.
    """
    return math.ceil(file_size / dtr)


def distance(object_1, object_2):
    """Computes the distance between two objects.

    Args:
        object_1 (object): first object.
        object_2 (object): second object.

    Returns:
        float: distance between the two objects.
    """
    return math.sqrt((object_1.X - object_2.X) ** 2 + (object_1.Y - object_2.Y) ** 2)
