from pipeline import Processor
from scipy.ndimage.filters import uniform_filter1d
import matplotlib.pyplot as plt
_colors = ['red', 'orange', 'yellow', 'green','cyan', 'blue', 'purple', 'crimson', 'black', 'gray']

def _plot_all_results(all_results, smooth_sz=10, smooth_sz_2=10):
    fig, ax = plt.subplots(1, 1)
    labels = []
    success = []
    colors = []
    for i, (h_name, rs) in enumerate(all_results):
        labels.append(h_name)
        colors.append(_colors[i])
        count = sum([res is not None for res in rs])
        success_rate = count / len(rs)
        success.append(success_rate)
    ax.barh(labels, width=success, color=colors)
    ax.set_title('Mean success rate')
    ax.set_xlabel('Success rate')
    plt.show()


class PlotSuccessRate(Processor):
    def process(self, all_results):
        _plot_all_results(all_results)
