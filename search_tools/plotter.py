smooth = lambda ys, n: uniform_filter1d(ys, n)
mean = lambda xs: sum(xs) / len(xs)

def plot_all_results(all_results, smooth_sz, smooth_sz_2):
    suboptimals = {}
    fig, (ax1, ax2) = plt.subplots(1, 2)
    
    for h_name, rs in all_results:
        sorted_rs = sorted(rs, key=lambda r:r.opt_len)
        sorted_rs = [i for i in sorted_rs if i.opt_len != 0]
        xs = [i.opt_len for i in sorted_rs]
        ys1 = [i.nodes_created for i in sorted_rs]
        ax1.plot(xs, smooth(ys1, smooth_sz), label=h_name)
        ax1.title.set_text('[Number of expanded (Y)] on [length of optimal path (X)]')
        
        ys2 = [i.act_len / i.opt_len for i in sorted_rs]
        ax2.plot(xs, smooth(ys2, smooth_sz_2), label=h_name)
        ax2.title.set_text('[Actual / Optimal lengths (Y)] on [length of optimal path (X)]')
        
        subs = [i.act_div_opt() for i in sorted_rs if i.act_div_opt() > 1]
        if len(subs) > 0:
            suboptimals[h_name] = subs
    
    for ax in (ax1, ax2): ax.legend()
    plt.show()
        
    if len(suboptimals) > 0:
        print('Suboptimals:')
        si = suboptimals.items()
        header = [''] + [h.replace('diagonal', 'diag') for h, _ in si]
        cnt = ['count'] + [f'{len(subopt)}' for _, subopt in si]
        cnt_prc = ['count %'] + [f'{100 * len(subopt)/len(all_results[0][1]):.1f} %' for _, subopt in si]
        worst_ratio = ['worst ratio'] + [f'{max(subopt):.2f}' for _, subopt in si]
        mean_ = ['mean subopt'] + [f'{mean(subopt):.2f}' for _, subopt in si]
        print(tabulate([header, cnt, cnt_prc, worst_ratio, mean_]))
