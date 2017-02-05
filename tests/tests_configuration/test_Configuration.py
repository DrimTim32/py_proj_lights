import os

import pytest

from core.configuration import config

norm = "euclidean"
variance = "variance"
importance = "log"
number_of_directions = 4

file_json = """{	"numberOfDirections": 4,
	"directions": [
		{	"Id": 0,
			"InLanes": 2,
			"OutLanes": 2,
            "Lanes": [
				{	"LaneId": 0,
					"TurnDirections": [
                      { "Direction": 1,
                        "Probability": 0.5,
                        "Safe": false
                      },
                      { "Direction": 2,
                        "Probability": 0.5,
                        "Safe": false
                      }]

				},
				{	"LaneId": 1,
					"TurnDirections": [
                      { "Direction": 3,
                        "Probability": 0.5,
                        "Safe": true
                      }]
				}
			]
		},
		{	"Id": 1,
			"InLanes": 2,
			"OutLanes": 2,
            "Lanes": [
				{	"LaneId": 0,
					"TurnDirections": [
                      { "Direction": 1,
                        "Probability": 0.5,
                        "Safe": false
                      },
                      { "Direction": 2,
                        "Probability": 0.5,
                        "Safe": false
                      }]


				},
				{	"LaneId": 1,
					"TurnDirections": [
                      { "Direction": 3,
                        "Probability": 0.5,
                        "Safe": false
                      }]

				}
			]
		},
		{	"Id": 2,
			"InLanes": 2,
			"OutLanes": 2,
            "Lanes": [
				{	"LaneId": 0,
					"TurnDirections": [
                      { "Direction": 1,
                        "Probability": 0.5,
                        "Safe": false
                      },
                      { "Direction": 2,
                        "Probability": 0.5,
                        "Safe": false
                      }]


				},
				{	"LaneId": 1,
					"TurnDirections": [
                      { "Direction": 2,
                        "Probability": 0.5,
                        "Safe": false
                      },
                      { "Direction": 3,
                        "Probability": 0.5,
                        "Safe": false
                      }]

				}
			]
		},
		{	"Id": 3,
			"InLanes": 2,
			"OutLanes": 2,
            "Lanes": [
				{	"LaneId": 0,
					"TurnDirections": [
                      { "Direction": 1,
                        "Probability": 0.5,
                        "Safe": false
                      },
                      { "Direction": 2,
                        "Probability": 0.5,
                        "Safe": false
                      }]

				},
				{	"LaneId": 1,
					"TurnDirections": [
                      { "Direction": 2,
                        "Probability": 0.5,
                        "Safe": false
                      },
                      { "Direction": 3,
                        "Probability": 0.5,
                        "Safe": false
                      }]

				}
			]
		}
	],
	"norm": "euclidean",
	"variance": "variance",
	"importance": "log"
}"""

def test_reading_from_file():
    text_file = open("test.json", "w")
    text_file.write(file_json)
    text_file.close()
    configuration = config.Config.from_config_file("test.json")
    assert configuration.number_of_directions == 4
    assert configuration.norm == norm
    assert configuration.variance == variance
    assert configuration.importance == importance
    assert configuration.directions_lanes == {0: [2, 2], 1: [2, 2], 2: [2, 2], 3: [2, 2]}
    assert configuration.directions_turns == {0: {0: {1: [0.5, False], 2: [0.5, False]}, 1: {3: [0.5, True]}}, 1: {0: {1: [0.5, False], 2: [0.5, False]}, 1: {3: [0.5, False]}}, 2: {0: {1: [0.5, False], 2: [0.5, False]}, 1: {2: [0.5, False], 3: [0.5, False]}}, 3: {0: {1: [0.5, False], 2: [0.5, False]}, 1: {2: [0.5, False], 3: [0.5, False]}}}
    os.remove("test.json")
