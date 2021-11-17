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

@dataclass
class Zoom:
    a:      Tuple[int, int]
    b:      Tuple[int, int]
    w:      int
    h:      int
    rotate: bool
        
    @staticmethod
    def no_zoom(m: MapMAI):
        return Zoom((0, 0), (m.width, m.height), m.width, m.width, False)
    
    @property
    def rotator(self): return -1 if self.rotate else 1
    
    def _size(self, scale): return (scale * self.w, scale * self.h)
    def size(self, scale): return self._size(scale)[::self.rotator]    
    
    def convert(self, c):
        x, y = c
        if self.a[0] <= x <= self.b[0] and self.a[1] <= y <= self.b[1]:
            new_c = (x - self.a[0], y - self.a[1])
            return new_c[::self.rotator]
        return None
        
    @staticmethod
    def calc_zoom(m, results):
        def flat_and_take(pos):
            for r in results: yield from map(lambda x:x[pos], r.iter_coords())

        a = min(flat_and_take(0)), min(flat_and_take(1))
        b = max(flat_and_take(0)), max(flat_and_take(1))
        c, d = m.size, 2
        aa = (max(0, a[0] - d), max(0, a[1] - d))
        bb = (min(c[0], b[0] + d), min(c[1], b[1] + d))
        w, h = bb[0] - aa[0], bb[1] - aa[1]
        return Zoom(aa, bb, w, h, h > w)

SC = 5

def mix_colors(col_a, col_b, beta):
    alpha = 1 - beta
    return tuple(int(alpha * a + beta * b) for a, b in zip(col_a, col_b))

def make_image(gmap: MapMAI, res: EnrichedRunResult, zoom):
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
        if not nodes: return
        for node in nodes: draw_node(node.coord, color)

    def draw_nodes_gradient(nodes, col_min, col_max):
        if not nodes: return
        max_time = max(n.time for n in nodes)
        mix_cols = lambda time: mix_colors(col_min, col_max, time / max_time)
        for node in nodes: draw_node(node.coord, mix_cols(node.time))

    for c, tp in gmap.iter_coords_types(): draw_node(c, COL_MAP[tp])
            
    draw_nodes(res.n_opened, Colors.GRAY_WHITE)
    draw_nodes_gradient(res.n_expanded, Colors.RED, Colors.GREEN)
    draw_nodes(res.path, Colors.BLUE)
    draw_node(res.task.start, Colors.RED)
    draw_node(res.task.goal, Colors.GREEN)
    
    return im

def draw_map(gmap: MapMAI, res: EnrichedRunResult, title, zoom=None):
    im = make_image(gmap, res, zoom)

    fig, ax = plt.subplots(dpi=150)
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    plt.title(title)
    plt.imshow(np.asarray(im))    
