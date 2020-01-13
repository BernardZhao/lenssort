from PIL import Image, ImageDraw
import face_recognition
import os.path
from pixelsort import pixelsort

from lenssort.masks import generate


def find_faces(file_path):
    try:
        image = face_recognition.load_image_file(file_path)
    except FileNotFoundError:
        print(f'Provided image file at "{file_path}" not found.')
    else:
        print("Looking for faces...")
        return face_recognition.face_landmarks(image), image


def lenssort(file_path, mask, invert, angle):
    name = os.path.basename(file_path)
    faces, image = find_faces(file_path)
    if not faces:
        print("No faces found.")
    else:
        print(f"{len(faces)} faces found in {name}")
        pil_image = Image.fromarray(image)
        mask_image, args = generate(faces, pil_image, mask, invert, angle)
        result_image = pixelsort(
            pil_image,
            mask_image=mask_image,
            **args
        )
        return result_image
