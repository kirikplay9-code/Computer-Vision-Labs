import matplotlib.pyplot as plt
import numpy as np


def show_histogram(image):
    arr = np.array(image)

    plt.figure()

    if image.mode == "L" or len(arr.shape) == 2:
        counts = np.bincount(arr.flatten(), minlength=256)
        plt.plot(counts, color="gray")
        plt.title("Гистограмма ЧБ")
    else:
        r = np.bincount(arr[:, :, 0].flatten(), minlength=256)
        g = np.bincount(arr[:, :, 1].flatten(), minlength=256)
        b = np.bincount(arr[:, :, 2].flatten(), minlength=256)

        plt.plot(r, color="red")
        plt.plot(g, color="green")
        plt.plot(b, color="blue")
        plt.title("RGB гистограмма")

    plt.xlim(0, 255)
    plt.grid()
    plt.show()