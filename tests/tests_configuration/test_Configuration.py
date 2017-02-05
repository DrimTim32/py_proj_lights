import os

import pytest

from core.configuration import config

norm = "euclidean"
variance = "variance"
importance = "log"
roads_length = 16

file_json = """{
  "directions": [
    {
      "Id": 0,
      "InLanes": 2,
      "OutLanes": 2,
      "Lanes": [
        {
          "TurnDirections": [
            {
              "Direction": 1,
              "Probability": 0.1,
              "Safe": false
            },
            {
              "Direction": 2,
              "Probability": 0.01,
              "Safe": false
            }
          ]
        },
        {
          "TurnDirections": [
            {
              "Direction": 3,
              "Probability": 0.01,
              "Safe": true
            }
          ]
        }
      ]
    },
    {
      "Id": 1,
      "InLanes": 2,
      "OutLanes": 2,
      "Lanes": [
        {
          "TurnDirections": [
            {
              "Direction": 1,
              "Probability": 0.01,
              "Safe": false
            },
            {
              "Direction": 2,
              "Probability": 0.01,
              "Safe": false
            }
          ]
        },
        {
          "TurnDirections": [
            {
              "Direction": 3,
              "Probability": 0.01,
              "Safe": false
            }
          ]
        }
      ]
    },
    {
      "Id": 2,
      "InLanes": 2,
      "OutLanes": 2,
      "Lanes": [
        {
          "TurnDirections": [
            {
              "Direction": 1,
              "Probability": 0.01,
              "Safe": false
            },
            {
              "Direction": 2,
              "Probability": 0.01,
              "Safe": false
            }
          ]
        },
        {
          "TurnDirections": [
            {
              "Direction": 3,
              "Probability": 0.01,
              "Safe": true
            }
          ]
        }
      ]
    },
    {
      "Id": 3,
      "InLanes": 2,
      "OutLanes": 2,
      "Lanes": [
        {
          "TurnDirections": [
            {
              "Direction": 1,
              "Probability": 0.01,
              "Safe": false
            },
            {
              "Direction": 2,
              "Probability": 0.01,
              "Safe": false
            }
          ]
        },
        {
          "TurnDirections": [
            {
              "Direction": 3,
              "Probability": 0.01,
              "Safe": true
            }
          ]
        }
      ]
    }
  ],
  "roads_length": 16,
  "norm": "euclidean",
  "variance": "variance",
  "importance": "log"
}"""

def test_reading_from_file():
    text_file = open("test.json", "w")
    text_file.write(file_json)
    text_file.close()
    configuration = config.Config.from_config_file("test.json")
    assert configuration.roads_length == roads_length
    assert configuration.norm == norm
    assert configuration.variance == variance
    assert configuration.importance == importance
    assert configuration.directions_lanes == {0: [2, 2], 1: [2, 2], 2: [2, 2], 3: [2, 2]}
    assert configuration.directions_turns == {0: [{1: [0.1, False], 2: [0.01, False]}, {3: [0.01, True]}], 1: [{1: [0.01, False], 2: [0.01, False]}, {3: [0.01, False]}], 2: [{1: [0.01, False], 2: [0.01, False]}, {3: [0.01, True]}], 3: [{1: [0.01, False], 2: [0.01, False]}, {3: [0.01, True]}]}

    os.remove("test.json")
