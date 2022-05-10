from tkinter import N


class Que:
    def __init__(self):
        self.data:dict = {}
        self.start = 0
        self.end = 0
    
    def __iter__(self):
        return self

    def __next__(self):
        r = self.get()
        if r != None:
            return r
        else:
            raise StopIteration()

    def append(self,n:object):
        if n != None:
            self.data[self.end] = n
            self.end += 1

    def get(self): 
        r = None
        try:
            i = self.start
            if self.start < self.end:
                self.start += 1
            r = self.data.pop(i)
        except BaseException:
            r = None
        return r
