class Size:
    def __init__(self, w: float, h: float) -> None:
        self.change_fuc = []
        self.updateSize(w, h)

    def __repr__(self):
        return "(%s, %s)" % (self.w, self.h)

    def __str__(self):
        return "(%s, %s)" % (self.w, self.h)

    def updateSize(self, w, h):
        self.w: float = w
        self.h: float = h
        self.x: float = w
        self.y: float = h
        for fuc in self.change_fuc:
            fuc(w, h)

    def onChange(self, fuc):
        self.change_fuc.append(fuc)
