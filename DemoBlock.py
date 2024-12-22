from pyglgame.BufferBuilder import *

SIZE_X = 8
SIZE_Y = 1
SIZE_Z = 16384

POINT_SIZE = 100

class DemoBlock:
    blocks:list[list[list["DemoBlock"]]] = [[[None for _3 in range(SIZE_Z)] for _2 in range(SIZE_Y)] for _1 in range(SIZE_X)]
    all_blocks:list["DemoBlock"] = []
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        if x < 0 or y < 0 or z < 0: raise Exception("Out of range")
        if x >= SIZE_X or y >= SIZE_Y or z >= SIZE_Z: raise Exception("Out of range")
        DemoBlock.blocks[x][y][z] = self
        DemoBlock.all_blocks.append(self)

    def topHasBlock(self)->bool:
        if self.y + 1 >= SIZE_Y: return False
        return DemoBlock.blocks[self.x][self.y + 1][self.z] is not None
    
    def downHasBlock(self)->bool:
        if self.y - 1 < 0: return False
        return DemoBlock.blocks[self.x][self.y - 1][self.z] is not None
    
    def leftHasBlock(self)->bool:
        if self.x - 1 < 0: return False
        return DemoBlock.blocks[self.x - 1][self.y][self.z] is not None
    
    def rightHasBlock(self)->bool:
        if self.x + 1 >= SIZE_X: return False
        return DemoBlock.blocks[self.x + 1][self.y][self.z] is not None
    
    def frontHasBlock(self)->bool:
        if self.z + 1 >= SIZE_Z: return False
        return DemoBlock.blocks[self.x][self.y][self.z + 1] is not None
    
    def backHasBlock(self)->bool:
        if self.z - 1 < 0: return False
        return DemoBlock.blocks[self.x][self.y][self.z - 1] is not None
        

    def addSurface(self, buf_builder: BufferBuilder):
        # 前
        if not self.frontHasBlock():
            buf_builder.pos(self.x + 0.5, self.y + 0.5, self.z + 0.5).col(1, 0, 0, 1).siz(POINT_SIZE).end()
            buf_builder.pos(self.x - 0.5, self.y + 0.5, self.z + 0.5).col(0, 1, 0, 1).siz(POINT_SIZE).end()
            buf_builder.pos(self.x - 0.5, self.y - 0.5, self.z + 0.5).col(0, 0, 1, 1).siz(POINT_SIZE).end()
            buf_builder.pos(self.x + 0.5, self.y - 0.5, self.z + 0.5).col(1, 1, 0, 1).siz(POINT_SIZE).end()
        # 后
        if not self.backHasBlock():
            buf_builder.pos(self.x + 0.5, self.y + 0.5, self.z - 0.5).col(1, 0, 0, 1).siz(POINT_SIZE).end()
            buf_builder.pos(self.x + 0.5, self.y - 0.5, self.z - 0.5).col(0, 1, 0, 1).siz(POINT_SIZE).end()
            buf_builder.pos(self.x - 0.5, self.y - 0.5, self.z - 0.5).col(0, 0, 1, 1).siz(POINT_SIZE).end()
            buf_builder.pos(self.x - 0.5, self.y + 0.5, self.z - 0.5).col(1, 1, 0, 1).siz(POINT_SIZE).end()
        # 左
        if not self.leftHasBlock():
            buf_builder.pos(self.x - 0.5, self.y + 0.5, self.z + 0.5).col(1, 0, 0, 1).siz(POINT_SIZE).end()
            buf_builder.pos(self.x - 0.5, self.y + 0.5, self.z - 0.5).col(0, 1, 0, 1).siz(POINT_SIZE).end()
            buf_builder.pos(self.x - 0.5, self.y - 0.5, self.z - 0.5).col(0, 0, 1, 1).siz(POINT_SIZE).end()
            buf_builder.pos(self.x - 0.5, self.y - 0.5, self.z + 0.5).col(1, 1, 0, 1).siz(POINT_SIZE).end()
        # 右
        if not self.rightHasBlock():
            buf_builder.pos(self.x + 0.5, self.y + 0.5, self.z + 0.5).col(1, 0, 0, 1).siz(POINT_SIZE).end()
            buf_builder.pos(self.x + 0.5, self.y - 0.5, self.z + 0.5).col(0, 1, 0, 1).siz(POINT_SIZE).end()
            buf_builder.pos(self.x + 0.5, self.y - 0.5, self.z - 0.5).col(0, 0, 1, 1).siz(POINT_SIZE).end()
            buf_builder.pos(self.x + 0.5, self.y + 0.5, self.z - 0.5).col(1, 1, 0, 1).siz(POINT_SIZE).end()
        # 上
        if not self.topHasBlock():
            buf_builder.pos(self.x + 0.5, self.y + 0.5, self.z + 0.5).col(1, 0, 0, 1).siz(POINT_SIZE).end()
            buf_builder.pos(self.x + 0.5, self.y + 0.5, self.z - 0.5).col(0, 1, 0, 1).siz(POINT_SIZE).end()
            buf_builder.pos(self.x - 0.5, self.y + 0.5, self.z - 0.5).col(0, 0, 1, 1).siz(POINT_SIZE).end()
            buf_builder.pos(self.x - 0.5, self.y + 0.5, self.z + 0.5).col(1, 1, 0, 1).siz(POINT_SIZE).end()
        # 下
        if not self.downHasBlock():
            buf_builder.pos(self.x + 0.5, self.y - 0.5, self.z + 0.5).col(1, 0, 0, 1).siz(POINT_SIZE).end()
            buf_builder.pos(self.x - 0.5, self.y - 0.5, self.z + 0.5).col(0, 1, 0, 1).siz(POINT_SIZE).end()
            buf_builder.pos(self.x - 0.5, self.y - 0.5, self.z - 0.5).col(0, 0, 1, 1).siz(POINT_SIZE).end()
            buf_builder.pos(self.x + 0.5, self.y - 0.5, self.z - 0.5).col(1, 1, 0, 1).siz(POINT_SIZE).end()



