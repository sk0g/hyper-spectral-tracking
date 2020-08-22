from sys import argv
from typing import *


def format_relative_coordinates(input_coordinates: List[int]) -> List[int]:
    """
    :param
        input_coordinates: Coordinates in the form of
            [x-top-left, y-top-left, x-bottom-right-offset, y-bottom-right-offset]
    :return:
        formatted coordinates in the form of
            [x-bottom-left, y-bottom-left, x-bottom-right, y-bottom-right,
            x-top-right, y-top-right, x-top-left, y-top-left]
    """
    if len(input_coordinates) != 4:
        raise ValueError

    [x, y, x_offset, y_offset] = input_coordinates

    return [
        x, y,
        x + x_offset, y,
        x + x_offset, y + y_offset,
        x, y + y_offset]


def create_vot_json_file(root_dir: str):
    """
    Creates VOT2018 style JSON file for a given root directory

    For each directory $d, append to JSON as follows:
    "$d": {
      "video_dir": "$1",
      "init_rect": [
        x-bottom-left,
        y-bottom-left,
        x-bottom-right,
        y-bottom-right,
        x-top-right,
        y-top-right,
        x-top-left,
        y-top-left
      ],
      "img_names": [
        "$d/subdir/img_name.jpg",
        ...
      ],
      "gt_rect": [
        [
          // ground truth co-ordinates, in same format as init_rect
        ]
      ],
      "camera_motion": [ 0, ... ], // WHERE (len == len(img_names) )
      "illum_change": [ 0, ... ],  // WHERE (len == len(img_names) )
      "motion_change": [ 0, ... ], // WHERE (len == len(img_names) )
      "size_change": [ 0, ... ],   // WHERE (len == len(img_names) )
      "occlusion": [ 0, ... ],     // WHERE (len == len(img_names) )
      "height": 123, //check actual value)
      "width": 123   //check actual value
    }
    """
    print(root_dir)


if __name__ == '__main__':
    if len(argv) == 2:
        path = argv[1]
        create_vot_json_file(path)
    else:
        print("Please provide path to root directory")
