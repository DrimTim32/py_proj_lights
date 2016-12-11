from Drawing.drawing_consts import *
from collections import namedtuple

RoadSizeVector = namedtuple('RoadSizeVector', ['len', 'inside_direction_count', 'outsize_direction_count'])


def get_empty_road(size_vector: RoadSizeVector):
    zero_count = size_vector.inside_direction_count
    one_count = size_vector.outsize_direction_count
    length = size_vector.len

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
        return 0 if len(self.first) == 0 else len(self.first[0])

    @property
    def length(self):
        return self.__len__()

    @property
    def width(self):
        return len(self.first) + len(self.second)

    @property
    def first_indexes(self):
        for i in range(len(self.first)):
            for q in range(len(self.first[i])):
                yield (i, q)

    @property
    def second_indexes(self):
        for i in range(len(self.second)):
            for q in range(len(self.second[i])):
                yield (i, q)
