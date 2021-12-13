from moving_ai.zoom import Zoom
from moving_ai.mai_map import MapMAI
from run_result import AreaRunResult
from processors.processor import AreaProcessor
import numpy as np
import imageio
# todo eliminate: just return image and draw it inside notebooks?
import matplotlib.pyplot as plt
from IPython.display import HTML
from node import Node

from PIL import Image, ImageDraw

class Colors:
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    GRAY = (100, 100, 100)
    GRAY_WHITE = (200, 200, 200)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    AQUA = (0, 255, 255)
    YELLOW = (255, 255, 0)
    BROWN = (165, 42, 42)
    CORAL = (255, 127, 80)
    LIGHTSEAGREEN = (32, 178, 170)

COL_MAP = {
    '.': Colors.WHITE,
    'G': Colors.GRAY_WHITE,
    '@': Colors.BLACK,
    'O': Colors.BLACK,
    'T': Colors.BROWN,
    'S': Colors.YELLOW,
    'W': Colors.AQUA
}

SC = 5 # scale

def mix_colors(col_a, col_b, beta):
    alpha = 1 - beta
    return tuple(int(alpha * a + beta * b) for a, b in zip(col_a, col_b))

# todo generalize #make_image and #make_images
def make_image(gmap: MapMAI, res: AreaRunResult, zoom):
    if not zoom: zoom = Zoom.no_zoom(gmap)
    
    im = Image.new('RGB', zoom.size(SC), color = 'white')
    draw = ImageDraw.Draw(im)
    
    def draw_node(c, color):
        c = zoom.convert(c)
        if not c: return
        x, y = c
        rec = (x * SC, y * SC, (x + 1) * SC - 1, (y + 1) * SC - 1)
        draw.rectangle(rec, fill=color, width=0)

    def draw_nodes(nodes, color):
        for c in (nodes.coords() if nodes else []):
            draw_node(c, color)

    def draw_nodes_gradient(nodes, col_min, col_max):
        if not nodes: return
        max_time = max(nodes.time(c) for c in nodes.coords())
        mix_cols = lambda time: mix_colors(col_min, col_max, time / max_time)
        for c in nodes.coords():
            draw_node(c, mix_cols(nodes.time(c)))

    for c, tp in gmap.iter_coords_types():
        draw_node(c, COL_MAP[tp])
            
    draw_nodes(res.n_opened, Colors.GRAY_WHITE)
    draw_nodes_gradient(res.n_expanded, Colors.RED, Colors.GREEN)
    draw_nodes(res.path, Colors.BLUE)
    draw_node(res.task.start_c, Colors.RED)
    draw_node(res.task.goal_c, Colors.GREEN)
    
    return im

# todo generalize #make_image and #make_images
def make_images(gmap: MapMAI, res: AreaRunResult, zoom, draw_step):
    if not zoom:
        zoom = Zoom.no_zoom(gmap)
    
    im = Image.new('RGB', zoom.size(SC), color = 'white')
    draw = ImageDraw.Draw(im)
    
    def draw_node(c, color):
        c = zoom.convert(c)
        if not c: return
        x, y = c
        draw.rectangle((x * SC, y * SC, (x + 1) * SC - 1, (y + 1) * SC - 1), fill=color, width=0)

    def draw_nodes(nodes, color):
        for c in (nodes.coords() if nodes else []):
            draw_node(c, color)

    def draw_nodes_gradient(nodes, col_min, col_max):
        if not nodes: return
        max_time = max(nodes.time(c) for c in nodes.coords())
        mix_cols = lambda time: mix_colors(col_min, col_max, time / max_time)

        for i, coord in enumerate(nodes.coords()):
            draw_node(coord, mix_cols(nodes.time(coord)))
            if i % draw_step == 0:
                yield im
        for _ in range(30):
            yield im
                

    for c, tp in gmap.iter_coords_types(): draw_node(c, COL_MAP[tp])

    draw_nodes(res.n_opened, Colors.GRAY_WHITE)
    draw_nodes(res.path, Colors.BLUE)
    draw_node(res.task.start_c, Colors.RED)
    draw_node(res.task.goal_c, Colors.GREEN)

    yield from draw_nodes_gradient(res.n_expanded, Colors.RED, Colors.GREEN)

def draw_map(gmap: MapMAI, res: AreaRunResult, title, zoom=None):
    im = make_image(gmap, res, zoom)

    fig, ax = plt.subplots(dpi=150)
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    plt.title(title)
    plt.imshow(np.asarray(im))

def save_map_gif(gmap: MapMAI, res: AreaRunResult, title, zoom=None, step=5):
    ims = make_images(gmap, res, zoom, step)
    return ims

def make_bold(string):
    return "\033[1m{}\033[0m".format(string)

def flatten(xss):
    return [x for xs in xss for x in xs]

class VisualizeMaiMap(AreaProcessor):
    def process_with_area(self, area, all_results):
        zoom = Zoom.calc_zoom(area, flatten([n_r[1] for n_r in all_results]))
        for a_name, rs in all_results:
            for er in rs:
                draw_map(area, er, a_name, zoom)

class VisualizeMaiMapGif(AreaProcessor):
    def __init__(self, step=5, duration=100, out_path_prefix='./output/walk'):
        super().__init__()
        self.step = step
        self.duration = duration
        self.out_path_prefix = out_path_prefix

    def process_with_area(self, area, all_results):
        zoom = Zoom.calc_zoom(area, flatten([n_r[1] for n_r in all_results]))
        i_paths = []
        gif_fmt = '<b>{}</b><br> {} <img src="{}" width="750" align="center">'
        html_parts = []
        for a_name, rs in all_results:
            for er in rs:
                a_name_upd = a_name.replace('*', 'star').replace('.', '_')
                i_path = f'{self.out_path_prefix}-{a_name_upd}.gif'
                ims_gen = make_images(area, er, zoom, self.step)

                with imageio.get_writer(i_path, mode='I') as fout:
                    for i in ims_gen:
                        fout.append_data(np.array(i))
                i_paths.append(i_path)
                report = er.report.replace('\n', '<br>\n')
                html_parts.append(gif_fmt.format(a_name, report, i_path))

        html = '\n'.join(html_parts)
        return HTML(html)
