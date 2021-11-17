from scipy import stats

import cloudpickle
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os, errno


def create_parent_dir(f_name):
    # Create Directory if Parent Directory does not exist
    if not os.path.exists(os.path.dirname(f_name)):
        try:
            os.makedirs(os.path.dirname(f_name))
        except OSError as exc:  # Guard against race condition
            print("Race Condition encoutered -- file cannot be saved")


def save_kde_cloudpickle(kernel, f_name):
    f_name = f"kde/{f_name}.cp.pkl"
    create_parent_dir(f_name)
    with open(f_name, "wb") as f:
        cloudpickle.dump(kernel, f)
    print(f'\nSaving KDE Model to {f_name}')


def get_kde(df):
    kernel = stats.gaussian_kde(
        np.vstack([df["latitude"], df["longitude"]]), bw_method="scott"
    )
    return kernel


"""
Plotting the kde hotspot using matplotlib
"""


def plot_kde(kernel, f_name, x_min=40.65, x_max=40.95, y_min=-74.04, y_max=-73.88):
    X, Y = np.mgrid[x_min:x_max:100j, y_min:y_max:100j]
    positions = np.vstack([X.ravel(), Y.ravel()])
    Z = np.reshape(kernel(positions).T, X.shape)

    fig, ax = plt.subplots()
    ax.imshow(
        np.rot90(Z), cmap=plt.cm.gist_earth_r, extent=[x_min, x_max, y_min, y_max]
    )

    ax.set_xlim(left=x_min, right=x_max)
    ax.set_ylim(bottom=y_min, top=y_max)

    create_parent_dir("images/{f_name}.png")
    plt.savefig(f"images/{f_name}.png")
    print(f'\nSaving KDE Plot to images/{f_name}.png')


def heatmap(img, points, sigma=20):
    k = (
        (np.min(img.shape[:2]))
        if (np.min(img.shape[:2]) % 2 == 1)
        else (np.min(img.shape[:2]) - 1)
    )
    mask = np.zeros(img.shape[:2])
    shape = mask.shape
    for i in range(points.shape[0]):
        # Check if inside the image
        if points[i, 0] < shape[0] and points[i, 1] < shape[1]:
            mask[int(points[i, 0]), int(points[i, 1])] += points[i, 2]
    # Gaussian blur the points to get a nice heatmap
    blur = cv2.GaussianBlur(mask, (k, k), sigma)
    blur = blur * 100 / np.max(blur)
    return blur
