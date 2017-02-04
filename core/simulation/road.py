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
        return list([None for _ in range(length)])

    def get_empty_array_of_arrays(count):
        return list([get_empty_array() for _ in range(count)])

    return Road([get_empty_array_of_arrays(out_lanes_count),
                 get_empty_array_of_arrays(in_lanes_count)])


class Road:
    def __init__(self, road_array):
        if len(road_array[0]) != 0 and len(min(road_array[0], key=len)) != len(max(road_array[0], key=len)):
            raise ValueError("Out lanes are not equal")
        if len(road_array[1]) != 0 and len(min(road_array[1], key=len)) != len(max(road_array[1], key=len)):
            raise ValueError("In lanes are not equal")
        self.out_lanes = road_array[0]
        self.in_lanes = road_array[1]

    def __len__(self):
        out_len = 0 if len(self.out_lanes) == 0 else len(self.out_lanes[0])
        in_len = 0 if len(self.in_lanes) == 0 else len(self.in_lanes[0])
        return max(in_len, out_len)

    def update_out(self):
        for lane_index in range(self.out_width):
            lane = self.out_lanes[lane_index]
            for i in range(self.__len__() - 1, 0, -1):
                lane[i] = lane[i - 1]

    def update_in(self, lane_index):
        for i in range(self.__len__() - 1, 0, -1):
            if self.in_lanes[lane_index][i] is None:
                self.in_lanes[lane_index][i] = self.in_lanes[lane_index][i - 1]
                self.in_lanes[lane_index][i - 1] = None

    def push_car_out(self, lane_index, car):
        self.out_lanes[lane_index][0] = car

    def push_car_in(self, lane_index, car):
        if self.in_lanes[lane_index][0] is None:
            self.in_lanes[lane_index][0] = car

    def pull_car(self, lane_index):
        car = self.in_lanes[lane_index][-1]
        self.in_lanes[lane_index][-1] = None
        return car

    def has_waiting_car(self, lane_index):
        return self.in_lanes[lane_index][-1]

    @property
    def length(self):
        return self.__len__()

    @property
    def out_width(self):
        return len(self.out_lanes)

    @property
    def in_width(self):
        return len(self.in_lanes)

    @property
    def width(self):
        return len(self.out_lanes) + len(self.in_lanes)

    @property
    def out_indexes(self):
        for lane_index in range(len(self.out_lanes)):
            for field_index in range(len(self.out_lanes[lane_index])):
                yield (lane_index, field_index)

    @property
    def in_indexes(self):
        for i in range(len(self.in_lanes)):
            for q in range(len(self.in_lanes[i])):
                yield (i, q)
