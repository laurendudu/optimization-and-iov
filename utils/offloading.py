import numpy as np

from .main import (
    get_closest_rsu,
    is_server_free,
    compatible,
    computation_time,
    data_transfer_time,
    migration_time,
    distance,
)


def task_offloading(
    tasks_bank: list,
    network: list,
) -> list:
    """Offloading process of the tasks.
    The tasks are offloaded to the closest RSU to them, which has not been visited before.
    In the end, the tasks have a history of computation times and migration times.

    Args:
        tasks_bank (list): list of tasks.
        network (list): list of RSUs.

    Returns:
        list: list of tasks with their history.
    """
    current_time = 0

    # while there are still tasks to be completed
    while not all(task.COMPLETED for task in tasks_bank):

        # check if any task is not completed and is not migrating
        if any(not task.COMPLETED and task.MIGRATION_TIME == 0 for task in tasks_bank):
            # shuffle the tasks bank
            np.random.shuffle(tasks_bank)
            task = next(
                task
                for task in tasks_bank
                if not task.COMPLETED and task.MIGRATION_TIME == 0
            )

            # if the task was not being migrated, fin the closest rsu to the task
            if task.RSU_HISTORY == []:
                # get the closest rsu to the task
                closest_rsu = get_closest_rsu(network, task, task.RSU_HISTORY)

                task.RSU_HISTORY.append(closest_rsu)

                # suppose the task is assigned at that rsu directly
                task.X = closest_rsu.X
                task.Y = closest_rsu.Y
            else:
                # get the last rsu the task was assigned to
                closest_rsu = task.RSU_HISTORY[-1]

            # if the rsu is free and compatible with the task, compute the task
            if is_server_free(closest_rsu) and compatible(closest_rsu, task):
                closest_rsu.STATE = "BUSY"
                task.COMPLETED = True
                # if the task is of type 'COMPUTATION', compute the computation time
                if task.TYPE == "COMPUTATION":
                    t_computation = computation_time(
                        task_length=task.LENGTH,
                        vm_nb=closest_rsu.ES.VM_NB,
                        vm_cpu=closest_rsu.ES.VM_CP,
                    )
                    closest_rsu.END_TIME = current_time + t_computation

                    task.COMPUTATION_HISTORY = t_computation
                # else (if the task is of type 'DATA TRANSFER'), compute the transfer time
                elif task.TYPE == "DATA TRANSFER":
                    t_data_transfer = data_transfer_time(
                        file_size=task.FILE_SIZE, dtr=closest_rsu.DTR
                    )
                    closest_rsu.END_TIME = current_time + t_data_transfer
                    task.COMPUTATION_HISTORY = t_data_transfer

            # if the rsu is busy or incompatible with the task, migrate the task
            else:
                # find the closest rsu to the task
                closest_rsu = get_closest_rsu(network, task, task.RSU_HISTORY)

                # add the closest rsu to the history of the task
                task.RSU_HISTORY.append(closest_rsu)

                # compute the migration time
                t_migration = migration_time(
                    file_size=task.FILE_SIZE,
                    distance=distance(task, closest_rsu),
                    dtr=closest_rsu.DTR,
                )

                # update the migration time of the task
                task.MIGRATION_TIME = t_migration
                # keep a record of the total migration time of the task
                task.MIGRATION_HISTORY += t_migration

                # update the coordinates of the task for when it will be migrated
                task.X = closest_rsu.X
                task.Y = closest_rsu.Y

        # check if any rsu should turn free at the current time
        for rsu in network:
            if rsu.STATE == "BUSY" and rsu.END_TIME == current_time:
                rsu.STATE = "IDLE"
                rsu.END_TIME = 0

        # remove a time unit from the migration time of each task if the migration time is greater than 0
        for task in tasks_bank:
            if task.MIGRATION_TIME > 0:
                task.MIGRATION_TIME -= 1

        # if a task has gone through all the RSU, reset its history
        for task in tasks_bank:
            if len(task.RSU_HISTORY) == len(network):
                task.RSU_HISTORY = []

        # update the current time
        current_time += 1

    return tasks_bank
