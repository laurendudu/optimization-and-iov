import matplotlib.pyplot as plt
import pandas as pd


def plot_network(network: pd.DataFrame) -> plt.show():

    # plot all the RSU in the network dataframe
    fig, ax = plt.subplots(figsize=(9, 7))

    # set the background light green
    ax.set_facecolor("#d3f0d3")

    # make the colour of the points depend on the number of ES_VM_CP and add a colourbar
    sc = ax.scatter(
        network["RSU_X"],
        network["RSU_Y"],
        s=(network["ES_VM_NB"] + 1)
        * 100,  # we add one to plot the points even if there is no ES
        c=network["ES_VM_CP"],
        cmap="plasma",
    )

    # add a title
    ax.set_title("RSUs from the generated network", size=15)

    # set the title of the colorbar
    plt.colorbar(sc).set_label("Edge Server Computing Power (MIPS)")

    return plt.show()


def plot_rsu_ids(network: pd.DataFrame, ids: list) -> plt.show():

    fig, ax = plt.subplots(figsize=(9, 7))

    # set the background light green
    ax.set_facecolor("#d3f0d3")

    # make the colour of the points depend on the number of ES_VM_CP and add a colourbar
    sc = ax.scatter(
        network["RSU_X"],
        network["RSU_Y"],
        c=network["ES_VM_CP"],
        cmap="plasma",
    )

    # add a title
    ax.set_title("RSUs from the generated network", size=15)

    # set the title of the colorbar
    plt.colorbar(sc).set_label("Edge Server Computing Power (MIPS)")
    # add the ids of the RSUs as labels if they are 95 or 37
    for i, txt in enumerate(network["RSU_ID"]):
        if txt in ids:
            ax.annotate(txt, (network["RSU_X"][i], network["RSU_Y"][i]))

    return plt.show()
