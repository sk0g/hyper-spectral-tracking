from sys import argv


def create_vot_json_file(root_dir: str):
    """
    Creates VOT2018 style JSON file for a given root directory
    """
    print(root_dir)


if __name__ == '__main__':
    if len(argv) == 2:
        path = argv[1]
        create_vot_json_file(path)
    else:
        print("Please provide path to root directory")
