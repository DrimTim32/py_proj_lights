from Drawing.drawing_consts import *


class Road:
    def __init__(self, array):
        self.first = array[0]
        self.second = array[1]

    def __len__(self):
        return 0 if len(self.first) == 0 else len(self.first[0]) * (
        BLOCK_SIZE + CAR_OFFSET)

    @property
    def length(self):
        return self.__len__()

    @property
    def width(self):
        return (len(self.first) + len(self.second)) * BLOCK_SIZE

    def get_first_indexes(self):
        for i in range(len(self.first)):
            for q in range(len(self.first[i])):
                yield (i, q)

    def get_second_indexes(self):
        for i in range(len(self.second)):
            for q in range(len(self.second[i])):
                yield (i, q)
