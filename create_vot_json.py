from sys import argv
import os
import json
from typing import *
from PIL import Image


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

    json_data: Dict[str, Any] = {}
    for (root, dirs, files) in os.walk(root_dir):
        if not root.endswith("RGB"):
            continue

        directory_data: Dict[str, Any] = {}
        class_name = root.split("/")[-2]  # second last item, since path ends in /RGB
        img_files = [f for f in files if f.endswith("jpg")]

        directory_data["video_dir"] = class_name

        # remove the relative directory, keep only the needed path info
        directory_data["img_names"] = [os.path.join(root.split(root_dir)[-1], img_name) for img_name in img_files]

        ground_truths = [line.strip().split("\t") for line in
                         open(os.path.join(root, "groundtruth_rect.txt"), "r").readlines()]
        directory_data["gt_rect"] = [
            format_relative_coordinates(
                [int(gt[0]), int(gt[1]), int(gt[2]), int(gt[3])])
            for gt in ground_truths]

        # First bounding box is used to initialise tracking
        directory_data["init_rect"] = directory_data["gt_rect"][0]

        # Dummy keys to be filled by arrays of 0s
        for key in ["camera_motion", "illum_change", "motion_change", "occlusion"]:
            directory_data[key] = [0, ] * len(img_files)

        random_image_path = os.path.join(root, img_files.pop())
        directory_data["width"], directory_data["height"] = Image.open(random_image_path).size

        json_data[class_name] = directory_data

    json.dump(
        obj=json_data,
        fp=open(
            os.path.join(root_dir, "vot2018.json"), "w")
    )


if __name__ == '__main__':
    if len(argv) == 2:
        path = argv[1]
        create_vot_json_file(path)
    else:
        print("Please provide path to root directory")
