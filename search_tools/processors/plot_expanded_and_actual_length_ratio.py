from pipeline import Processor
from scipy.ndimage.filters import uniform_filter1d
import matplotlib.pyplot as plt

_smooth = lambda ys, n: uniform_filter1d(ys, n)

def _plot_all_results(all_results, smooth_sz = 10, smooth_sz_2 = 10):
    fig, (ax1, ax2) = plt.subplots(1, 2)
    
    for h_name, rs in all_results:
        # expected sorted results
        sorted_rs = rs
        xs = [i.opt_len for i in sorted_rs]
        ys1 = [i.nodes_created for i in sorted_rs]
        ax1.plot(xs, _smooth(ys1, smooth_sz), label=h_name)
        ax1.title.set_text('[Number of expanded (Y)] on [length of optimal path (X)]')
        
        ys2 = [i.act_len / i.opt_len for i in sorted_rs]
        ax2.plot(xs, _smooth(ys2, smooth_sz_2), label=h_name)
        ax2.title.set_text('[Actual / Optimal lengths (Y)] on [length of optimal path (X)]')
        
    for ax in (ax1, ax2):
        ax.legend()
    plt.show()

class PlotExpandedAndActualLengthRatio(Processor):
    def __init__(self, smooth=(10, 10)):
        self.smooth = smooth

    def process(self, all_results):
        _plot_all_results(all_results, *self.smooth)
