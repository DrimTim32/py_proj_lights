from Drawing.drawing_consts import *


class RoadSizeVector:
    def __init__(self, len, inside_direction_count=1,
                 outsize_direction_count=1):
        self.len = len
        self.inside_direction_count = inside_direction_count
        self.outsize_direction_count = outsize_direction_count


def get_empty_road(sizeVector: RoadSizeVector):
    zero_count = sizeVector.inside_direction_count
    one_count = sizeVector.outsize_direction_count
    length = sizeVector.len

    def get_empty_array():
        return list([0 for _ in range(length)])

    def get_empty_array_of_arrays(count):
        return list([get_empty_array() for _ in range(count)])

    return Road([get_empty_array_of_arrays(zero_count),
                 get_empty_array_of_arrays(one_count)])


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
