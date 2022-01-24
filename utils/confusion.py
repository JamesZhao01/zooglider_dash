import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support
from sklearn.preprocessing import normalize
from pylab import mpl
from matplotlib.colors import LinearSegmentedColormap, Normalize
from datetime import datetime


class MidpointNormalize(Normalize):
    r"""Normalize data around a midpoint."""

    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))


def render_confusion_matrix_from_csv(class_csv, cm_csv, fig_filename, fig_title):
    class_df = pd.read_csv(class_csv, index_col=0, low_memory=False)
    cm_df = pd.read_csv(cm_csv, index_col=0, low_memory=False)
    cm = cm_df.to_numpy()
    class_list = cm_df.index.values
    render_confusion_matrix(cm, class_df, fig_filename, fig_title, class_list)


def render_confusion_matrix(cm, class_df, fig_filename=None, fig_title=None, class_list=None):
    r"""Render confusion matrix and save to file. Includes classwise precision/recall

    Args:
        confusion_matrix (``ndarray``): The confusion matrix whose i-th row and
            j-th column entry indicates the number of samples with true label
            being i-th class and predicted label being j-th class.
        fig_filename (str): The absolute or relative path to save the
            visualized confusion matrix to.
        fig_title: The title to title the confusion matrix as.
        class_list: The list of class names to display on the confusion matrix.
    """
    norm_cm = normalize(cm, norm="l1", axis=1) * -1

    ground_truths = list(class_df["Ground Truth"])
    predicted_labels = list(class_df["Prediction"])
    # precison, recall, and f1 score
    # Jan 9: This is not returning a value for all classes when there are very few
    # examples, so changing to per-class prediciton which is probably better anyways
    #tupe = precision_recall_fscore_support(ground_truths, predicted_labels, zero_division=1)
    # recall_scores=tupe[1]

    classwise = precision_recall_fscore_support(ground_truths, predicted_labels,
                                                average=None, zero_division=0,
                                                labels=class_list)
    precision_scores = classwise[0]
    recall_scores = classwise[1]
    prfs = precision_recall_fscore_support(ground_truths, predicted_labels,
                                           average="weighted", zero_division=0)

    # Create a canvas and reasonable defaults
    fig = plt.figure(figsize=(23, 23), dpi=300)
    mpl.rcParams["lines.linewidth"] = 2
    mpl.rcParams["lines.markeredgewidth"] = 2
    mpl.rcParams["legend.markerscale"] = 1.2

    # Want color scale to go from dark green to grey-white to red
    CDICT = {
        "red": ((0.0, 1.0, 1.0), (0.5, 0.9, 0.9), (1.0, 0.0, 1.0)),
        "green": ((0.0, 1.0, 0.0), (0.5, 0.9, 0.9), (1.0, 0.6, 0.0)),
        "blue": ((0.0, 1.0, 0.0), (0.5, 0.9, 0.9), (1.0, 0.0, 1.0)),
    }

    # Initialize the plot
    ax = fig.add_subplot(1, 1, 1)
    # Save timestamp as "dd MMM yyyy" where MMM is the month as a three-letter abbreviation
    timestamp = datetime.now().strftime("%d %b %Y")
    ax.set_title(f"Confusion Matrix ({timestamp})\n{fig_title}\n" + "precision:" + f'{prfs[0]:.5f}' + "\n" +
                 "recall:" + f'{prfs[1]:.5f}' + "\n" + "f1 score:" + f'{prfs[2]:.5f}', fontsize=20, pad=100)
    ax.set_aspect(1)

    # Get the values from the csv, normalize them down the columns of the CM
    norm_cm = normalize(cm, norm="l1", axis=1) * -1

    # Invert off-axis values, assuming square
    for i in range(len(norm_cm)):
        norm_cm[i][i] = norm_cm[i][i] * -1

    # Add the class labels to each of the x and y axis
    # By convention sometimes classnames have _, remove for readability
    class_labels = [p.replace("_", " ") for p in class_list]
    plt.tick_params(axis="both", which="major", labelsize=18)
    ax.set_xticklabels(class_labels)
    ax.set_yticklabels(class_labels)
    plt.xlabel("Predicted", size=24)
    plt.ylabel("True", size=24)
    plt.xticks(
        np.arange(0, len(class_list), 1.0),
        rotation="vertical",
        horizontalalignment="center",
        verticalalignment="top",
        multialignment="right",
    )
    plt.yticks(
        np.arange(0, len(class_list), 1.0),
        horizontalalignment="right",
        verticalalignment="center",
        multialignment="right",
    )

    cm_map = LinearSegmentedColormap("WhiteRed", CDICT)

    norm = MidpointNormalize(midpoint=0)
    res = ax.imshow(
        np.array(norm_cm),
        norm=norm,
        cmap=cm_map,
        interpolation="none",
        vmin=-0.2,
        vmax=1,
    )
    width, height = cm.shape
    cb = fig.colorbar(res, shrink=0.72)
    cb_ticks = [-0.2, 0, 0.2, 0.4, 0.6, 0.8, 1.0]
    cb.ax.tick_params(labelsize=18)
    cb.set_ticks(cb_ticks)

    # Create the numbers in each cell
    for x in range(width):
        for y in range(height):
            ax.annotate(
                str(cm[x][y]),
                xy=(y, x),
                horizontalalignment="center",
                verticalalignment="center",
                color="white",
                size="12",
            )

    #width, height = cm.shape
    # add the recall for each class
    ax.text(width+0.5, -1, 'Recall', horizontalalignment="center",
            verticalalignment="center", color="black", fontsize="12")
    for x in range(width):
        ax.text(width+0.5, x,
                str(f'{recall_scores[x]:.2f}'),
                horizontalalignment="center",
                verticalalignment="center",
                color="black",
                fontsize="12")

    # add the precision for each class
    ax.text(-1, -1.1, 'Precision', rotation='vertical', horizontalalignment="center",
            verticalalignment="bottom", color="black", fontsize="12")
    for x in range(width):
        ax.text(x, -2,
                str(f'{precision_scores[x]:.2f}'),
                rotation='vertical',
                horizontalalignment="center",
                verticalalignment="center",
                color="black",
                fontsize="12")

    # Save out the file
    fig.tight_layout()
    # Tweak to prevent clipping of tick labels
    plt.subplots_adjust(bottom=0.16, top=1, left=0.30, right=1.0)
    if fig_filename:
        plt.savefig(fig_filename, format="png")
    return fig
