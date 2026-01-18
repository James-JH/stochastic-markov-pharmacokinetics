import numpy as np

def forward_eqs(p, t, Q):
    """
    Kolmogorov Forward Equation for CTMC
    """
    return np.dot(p, Q)

def plot_line(x, ys, labels, title="", xlabel="", ylabel=""):
    import matplotlib.pyplot as plt
    for y, label in zip(ys, labels):
        plt.plot(x, y, label=label)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_box(results, title="", ylabel="AUC"):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(8, 4))
    plt.boxplot([results[k] for k in results.keys()], labels=results.keys())
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()
