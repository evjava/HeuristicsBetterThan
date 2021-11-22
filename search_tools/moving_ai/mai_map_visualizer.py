from moving_ai.zoom import Zoom
from moving_ai.mai_map import MapMAI
from run_result import EnrichedRunResult
from processors.processor import AreaProcessor
# todo eliminate: just return image and draw it inside notebooks?
import matplotlib.pyplot as plt
import numpy as np

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

def make_image(gmap: MapMAI, res: EnrichedRunResult, zoom):
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
        if not nodes: return
        for node in nodes:
            draw_node(node.coord, color)

    def draw_nodes_gradient(nodes, col_min, col_max):
        if not nodes: return
        max_time = max(n.time for n in nodes)
        mix_cols = lambda time: mix_colors(col_min, col_max, time / max_time)
        for node in nodes:
            draw_node(node.coord, mix_cols(node.time))

    for c, tp in gmap.iter_coords_types():
        draw_node(c, COL_MAP[tp])
            
    draw_nodes(res.n_opened, Colors.GRAY_WHITE)
    draw_nodes_gradient(res.n_expanded, Colors.RED, Colors.GREEN)
    draw_nodes(res.path, Colors.BLUE)
    draw_node(res.task.start_c, Colors.RED)
    draw_node(res.task.goal_c, Colors.GREEN)
    
    return im

def draw_map(gmap: MapMAI, res: EnrichedRunResult, title, zoom=None):
    im = make_image(gmap, res, zoom)

    fig, ax = plt.subplots(dpi=150)
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    plt.title(title)
    plt.imshow(np.asarray(im))    

make_bold = lambda s: "\033[1m" + s + "\033[0m"

def flatten(xss):
    return [x for xs in xss for x in xs]

class VisualizeMaiMap(AreaProcessor):
    def process_with_area(self, area, all_results):
        zoom = Zoom.calc_zoom(area, flatten([n_r[1] for n_r in all_results]))
        for a_name, rs in all_results:
            for er in rs:
                draw_map(area, er, a_name)
