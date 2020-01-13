from lenssort.main import lenssort
from lenssort.masks import mask_types
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Detects faces in image and applies glitch effects.")
    parser.add_argument("file_path", help="Image file to edit.")
    parser.add_argument(
        "-m",
        "--mask",
        choices=mask_types.keys(),
        help="Mask of area to apply effects.")
    parser.add_argument("-a", "--angle", type=int, help="Angle to sort on.")
    parser.add_argument(
        "-i",
        "--invert",
        action='store_true',
        default=False,
        help="Invert selected area to be glitched.")
    parser.add_argument("-o", "--output", help="Image output path.")
    return vars(parser.parse_args())


args = parse_arguments()
output_path = args.pop("output")
result = lenssort(**args)
if output_path:
    result.save(output_path)
else:
    result.show()
