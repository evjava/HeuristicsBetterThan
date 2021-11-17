class RunContext:
    def __init__(area):
        self.area = area

    def get_neighbors(self, coord):
        return self.area.get_neighbors(*coord)
