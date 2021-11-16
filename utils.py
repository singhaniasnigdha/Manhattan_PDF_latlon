from scipy import stats

import cloudpickle
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def save_kde_cloudpickle(kernel, f_name):
    with open(f"{f_name}.cp.pkl", "wb") as f:
        cloudpickle.dump(kernel, f)


def get_kde(df):
    kernel = stats.gaussian_kde(
        np.vstack([df["latitude"], df["longitude"]]), bw_method="scott"
    )
    return kernel


"""
Plotting the kde hotspot using matplotlib
"""


def plot_kde(kernel, x_min=40.65, x_max=40.95, y_min=-74.04, y_max=-73.88):
    X, Y = np.mgrid[x_min:x_max:100j, y_min:y_max:100j]
    positions = np.vstack([X.ravel(), Y.ravel()])
    Z = np.reshape(kernel(positions).T, X.shape)

    fig, ax = plt.subplots()
    ax.imshow(
        np.rot90(Z), cmap=plt.cm.gist_earth_r, extent=[x_min, x_max, y_min, y_max]
    )

    ax.set_xlim(left=x_min, right=x_max)
    ax.set_ylim(bottom=y_min, top=y_max)
    plt.show()
