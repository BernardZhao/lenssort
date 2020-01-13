from PIL import ImageDraw, Image, ImageOps
from functools import reduce
import operator
import random
import math
import numpy as np

"""
facial_features = [
    'chin',
    'left_eyebrow',
    'right_eyebrow',
    'nose_bridge',
    'nose_tip',
    'left_eye',
    'right_eye',
    'top_lip',
    'bottom_lip'
]
"""


def generate(faces, image, mask_type, invert, angle):
    """
    Creates a mask file outlining desired parts of image and face.
    """
    print("Generating image face mask...")
    mask = Image.new("L", image.size)
    d = ImageDraw.Draw(mask)

    if mask_type is None:
        print("No mask provided, choosing a random mask.")
        mask_type = random.choice(list(mask_types.keys()))

    default_args = {
        "interval_function": "random",
        "sorting_function": "intensity",
        "clength": min(mask.size) // 20
    }
    args = mask_types[mask_type](mask, d, faces)
    args = args if args else {}
    # Force override with user options
    if angle:
        args["angle"] = angle

    return ImageOps.invert(mask) if invert else mask, {**default_args, **args}


def eyes(mask, d, faces):
    for face in faces:
        d.polygon(face["left_eye"], fill=255)
        d.polygon(face["right_eye"], fill=255)


def face(mask, d, faces):
    for face in faces:
        d.polygon(
            list(
                reversed(
                    face["left_eyebrow"])) +
            face["chin"] +
            list(
                reversed(
                    face["right_eyebrow"])),
            fill=255)


def shuffle(mask, d, faces):
    for face in faces:
        points = reduce(operator.concat, face.values())
        random.shuffle(points)
        d.polygon(points, fill=255)
    return {
        "interval_function": "none"
    }


def censored(mask, d, faces):
    for face in faces:

        p1 = np.array(face["left_eye"][0])
        p2 = np.array(face["right_eye"][3])
        p3 = np.array(face["left_eye"] + face["right_eye"])
        distances = np.cross(p2 - p1, p3 - p1) / np.linalg.norm(p2 - p1)
        width = math.ceil(abs(max(distances, key=abs)))

        dxdy = tuple(
            x - y for x,
            y in zip(
                face["left_eye"][0],
                face["right_eye"][3]))
        left = tuple(x + y * .6 for x, y in zip(face["left_eye"][0], dxdy))
        right = tuple(x - y * .6 for x, y in zip(face["right_eye"][3], dxdy))

        d.line([left, right], fill=255, width=width * 5)
    return {
        "clength": abs(max(dxdy, key=abs)),
    }


def facemask(mask, d, faces):
    for face in faces:
        diff = min(mask.size) // 20
        points = [face['nose_bridge'][0]] + face["left_eye"][3:] + [face["left_eye"]
                                                                    [0]] + face["chin"] + face["right_eye"][3:] + [face["right_eye"][0]]
        d.polygon(points, fill=255)
        d.polygon(
            list(map(lambda pair: (pair[0], pair[1] + diff), points)), fill=255)

    return {
        "clength": diff * 1.25,
        "angle": 90,
    }


def tears(mask, d, faces):
    for face in faces:
        lx = list(map(lambda x: x[0], face["left_eye"]))
        rx = list(map(lambda x: x[0], face["right_eye"]))
        dy = list(map(lambda x: x[1], face["chin"] +
                      face["left_eyebrow"] + face["right_eyebrow"]))
        diff = max(dy) - min(dy)

        for index, x in enumerate(range(min(lx), max(lx) + 1)):
            minfloor = max(face["left_eye"], key=lambda x: x[1])[1]
            maxfloor = face['nose_bridge'][-1][1]
            avg = (max(lx) + 1 - min(lx)) / 2
            ratio = abs((avg - index) / avg)
            floor = minfloor + (maxfloor - minfloor) * ratio
            y = int(random.triangular(floor, floor + 2 * diff * ratio, floor))
            d.line([(x, minfloor), (x, y)], fill=255, width=1)
            d.polygon(face["left_eye"][3:] + [face["left_eye"][0],
                                              (min(lx), minfloor), (max(lx) + 1, minfloor)], fill=255)

        for index, x in enumerate(range(min(rx), max(rx) + 1)):
            minfloor = max(face["right_eye"], key=lambda x: x[1])[1]
            maxfloor = face['nose_bridge'][-1][1]
            avg = (max(rx) - min(rx)) / 2
            ratio = abs((avg - index) / avg)
            floor = minfloor + (maxfloor - minfloor) * ratio
            y = int(random.triangular(floor, floor + 2 * diff * ratio, floor))
            d.line([(x, minfloor), (x, y)], fill=255, width=1)
            d.polygon(face["right_eye"][3:] + [face["right_eye"][0],
                                               (min(rx), minfloor), (max(rx) + 1, minfloor)], fill=255)

    return {
        "angle": 90,
        "clength": mask.size[1] // 20
    }


mask_types = {
    'eyes': eyes,
    'face': face,
    'shuffle': shuffle,
    'censored': censored,
    'facemask': facemask,
    'tears': tears,
}
