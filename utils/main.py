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


def get_closest_rsu(rsu_list: list, rsu_id: int) -> int:
    """Returns the index of the closest RSU in the list.

    Args:
        rsu_list (list): list of RSUs.
        rsu (int): RSU to compare.

    Returns:
        int: index of the closest RSU.
    """
    min_distance = math.inf
    min_index = -1
    rsu = rsu_list[rsu_id]
    for i in rsu_list.keys():
        if i != rsu_id:
            distance = math.sqrt(
                (rsu_list[i]["RSU_X"] - rsu["RSU_X"]) ** 2
                + (rsu_list[i]["RSU_Y"] - rsu["RSU_Y"]) ** 2
            )
            if distance < min_distance:
                min_distance = distance
                min_index = i
    return min_index
