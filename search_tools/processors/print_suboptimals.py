from pipeline import Processor
from tabulate import tabulate

_mean = lambda xs: sum(xs) / len(xs)

class PrintSuboptimals(Processor):
    def process(self, all_results):
        suboptimals = {}
        for h_name, rs in all_results:
            sorted_rs = rs
            subs = [i.act_div_opt() for i in sorted_rs if i.act_div_opt() > 1]
            if len(subs) > 0:
                suboptimals[h_name] = subs

        if len(suboptimals) == 0:
            return

        print('Suboptimals:')
        si = suboptimals.items()
        header = [''] + [h.replace('diagonal', 'diag') for h, _ in si]
        cnt = ['count'] + [f'{len(subopt)}' for _, subopt in si]
        cnt_prc = ['count %'] + [f'{100 * len(subopt)/len(all_results[0][1]):.1f} %' for _, subopt in si]
        worst_ratio = ['worst ratio'] + [f'{max(subopt):.2f}' for _, subopt in si]
        mean_ = ['mean subopt'] + [f'{_mean(subopt):.2f}' for _, subopt in si]
        print(tabulate([header, cnt, cnt_prc, worst_ratio, mean_]))

