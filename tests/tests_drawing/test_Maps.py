from Drawing import Map, Position

from Drawing import RoadSizeVector
def test_points_calculation():
    top_vector = RoadSizeVector(5,2,1)
    left_vector = RoadSizeVector(7,1,1)
    down_vector = RoadSizeVector(9,3,1)
    bottom_vector = RoadSizeVector(3,3,2)
    map = Map([top_vector,left_vector,down_vector,bottom_vector])