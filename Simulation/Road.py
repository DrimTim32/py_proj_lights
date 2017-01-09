from collections import namedtuple

RoadSizeVector = namedtuple('RoadSizeVector', ['length', 'out_lanes_count', 'in_lanes_count'])


def get_empty_road(size_vector):
    """
    :type size_vector : RoadSizeVector
    :return:
    """
    out_lanes_count = size_vector.out_lanes_count
    in_lanes_count = size_vector.in_lanes_count
    length = size_vector.length

    def get_empty_array():
        return list([0 for _ in range(length)])

    def get_empty_array_of_arrays(count):
        return list([get_empty_array() for _ in range(count)])

    return Road([get_empty_array_of_arrays(out_lanes_count),
                 get_empty_array_of_arrays(in_lanes_count)])


class Road:
    def __init__(self, road_array):
        self.out_lanes = road_array[0]
        self.in_lanes = road_array[1]

    def __len__(self):
        return 0 if len(self.out_lanes) == 0 else len(self.out_lanes[0])

    @property
    def length(self):
        return self.__len__()

    @property
    def width(self):
        return len(self.out_lanes) + len(self.in_lanes)

    @property
    def out_indexes(self):
        for i in range(len(self.out_lanes)):
            for q in range(len(self.out_lanes[i])):
                yield (i, q)

    @property
    def in_indexes(self):
        for i in range(len(self.in_lanes)):
            for q in range(len(self.in_lanes[i])):
                yield (i, q)
