"""
File containing Road class and supporting tools
"""
from collections import namedtuple

RoadSizeVector = namedtuple('RoadSizeVector', ['length', 'out_lanes_count', 'in_lanes_count'])


def get_empty_road(size_vector):
    """
    :param size_vector: road properties vector
    :type size_vector : RoadSizeVector
    :return: empty Road
    :rtype: Road
    """
    out_lanes_count = size_vector.out_lanes_count
    in_lanes_count = size_vector.in_lanes_count
    length = size_vector.length

    def get_empty_list():
        """
        :return: empty list
        :rtype: list[None]
        """
        return list([None for _ in range(length)])

    def get_empty_list_of_lists(count):
        """
        :param count: number of lists
        :return: list of empty lists
        :rtype: list[list[None]]
        """
        return list([get_empty_list() for _ in range(count)])

    return Road([get_empty_list_of_lists(out_lanes_count),
                 get_empty_list_of_lists(in_lanes_count)])


class Road:
    """
    Road class
    """

    def __init__(self, road_list):
        """
        initializes road from lists of lanes
        :param road_list: list of lanes
        :type road_list list[list[list[Car]]]
        """
        if len(road_list[0]) != 0 and len(min(road_list[0], key=len)) != len(max(road_list[0], key=len)):
            raise ValueError("all out lanes must have equal length")
        if len(road_list[1]) != 0 and len(min(road_list[1], key=len)) != len(max(road_list[1], key=len)):
            raise ValueError("all in lanes must have equal length")
        if len(road_list[0]) != len(road_list[1]):
            raise ValueError("In and Out lanest must have equal length")
        self.out_lanes = road_list[0]
        self.in_lanes = road_list[1]

    def __len__(self):
        out_len = 0 if len(self.out_lanes) == 0 else len(self.out_lanes[0])
        in_len = 0 if len(self.in_lanes) == 0 else len(self.in_lanes[0])
        return max(in_len, out_len)

    def update_out(self):
        """
        updates positions of cars going out of intersection
        :return: none
        """
        for lane_index in range(self.out_width):
            lane = self.out_lanes[lane_index]
            for i in range(self.__len__() - 1, 0, -1):
                lane[i] = lane[i - 1]
            lane[0] = None

    def update_in(self, lane_index):
        """
        updates posiitons of cars arriving intersection
        :param lane_index: index of lane to perform update on
        :return: none
        """
        for i in range(self.__len__() - 1, 0, -1):
            if self.in_lanes[lane_index][i] is None:
                self.in_lanes[lane_index][i] = self.in_lanes[lane_index][i - 1]
                self.in_lanes[lane_index][i - 1] = None
            else:
                self.in_lanes[lane_index][i].waiting_time += 1

    def push_car_out(self, lane_index, car):
        """
        pushes car from intersection to specific lane on out_road
        :param lane_index: index of lane
        :param car: car tu push on road
        :return: none
        """
        self.out_lanes[lane_index][0] = car

    def push_car_in(self, lane_index, car):
        """
        pushes car arriving to intersection to specific lane on in_road
        :param lane_index: index of lane
        :param car: car tu push on road
        :return: none
        """
        if self.in_lanes[lane_index][0] is None:
            self.in_lanes[lane_index][0] = car

    def pull_car(self, lane_index):
        """
        Pulls car from specific lane on road to intersection
        :param lane_index: index of lane
        :return: pulled car
        :rtype: Car
        """
        car = self.in_lanes[lane_index][-1]
        self.in_lanes[lane_index][-1] = None
        return car

    def has_waiting_car(self, lane_index):
        """
        Checks if there is a car waiting to enter intersection on specific lane
        :param lane_index: index of lane
        :return: if there is a car waiting to enter intersection
        :rtype: bool
        """
        return self.in_lanes[lane_index][-1]

    @property
    def length(self):
        """
        :return: length of the road
        :rtype: int
        """
        return self.__len__()

    @property
    def out_width(self):
        """
        :return: number of out lanes
        :rtype: int
        """
        return len(self.out_lanes)

    @property
    def in_width(self):
        """
        :return: number of in lanes
        :rtype: int
        """
        return len(self.in_lanes)

    @property
    def width(self):
        """
        :return: number of lanes
        :rtype: int
        """
        return len(self.out_lanes) + len(self.in_lanes)

    @property
    def out_indexes(self):
        """
        :return: out indexes
        """
        for lane_index in range(len(self.out_lanes)):
            for field_index in range(len(self.out_lanes[lane_index])):
                yield (lane_index, field_index)

    @property
    def in_indexes(self):
        """
        :return: in indexes
        """
        for i in range(len(self.in_lanes)):
            for j in range(len(self.in_lanes[i])):
                yield (i, j)
