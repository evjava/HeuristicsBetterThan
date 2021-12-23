from pipeline import Processor
import numpy as np
from scipy.ndimage.filters import uniform_filter1d
import matplotlib.pyplot as plt
_colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']

def _plot_all_results(all_results):
    fig, ax = plt.subplots(1, 1)
    expanded = []
    labels = []
    colors = []
    for i, (h_name, rs) in enumerate(all_results):
        labels.append(h_name)
        expanded.append(np.mean([res.nodes_created for res in rs if res is not None]))
        colors.append(_colors[i])
    ax.barh(labels, width=expanded, color=colors)
    ax.set_title('Mean expansions')
    ax.set_xlabel('nodes expanded')
    plt.show()


class PlotMeanExpanded(Processor):
    def process(self, all_results):
        _plot_all_results(all_results)
