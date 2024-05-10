import glob
import json
import os.path
from typing import List, Union, Tuple

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageOps

BOX_COLOR = "magenta"  # Color of the bbox
BACKGROUND_COLOR = "white"  # Background color of canvas


def read_scene(image_path: str) -> Tuple[Image, List]:
    """
    Reads the scene image and annotations & returns it
    Args:
        image_path (str): scene image path
    Returns:
        scene image and annotation box coordinates
    """
    scene_image = ImageOps.exif_transpose(Image.open(image_path))
    scene_annotations = json.load(open(scene_image_path
                                 .replace("images", "annotations")
                                 .replace("jpg", "json"), "r"))
    scene_boxes = list(map(lambda x: list(x.values()), scene_annotations))
    return scene_image, scene_boxes


def draw_boxes(canvas: Image,
               boxes: List,
               color: Union[Tuple, str] = BOX_COLOR,
               line_width: int = 8) -> Image:
    """
    Draws a box on image
    Args:
        canvas (Image): Image: drawing image
        boxes (List[int]): list of box coordinates
        color (Tuple): Color of the bbox
        line_width (int): Width of the surrounding line
    Return:
        Annotation boxes drawn image
    """
    try:
        draw_image = ImageDraw.Draw(canvas)
        for box in boxes:
            draw_image.rectangle(box, outline=color, width=line_width)
    except Exception as exc:
        raise Exception(f"Exception while drawing box: {exc}")
    return image


if __name__ == '__main__':

    for scene_no in range(1, 101):
        scene_no_str = str(scene_no)
        cv2.namedWindow(f"Scene {scene_no_str}", cv2.WINDOW_NORMAL)
        cv2.resizeWindow(f"Scene {scene_no_str}", 1080, 1920)
        scene_image_paths = sorted(glob.glob(os.path.join("scenes", scene_no_str, "images", "*.jpg")))
        scene_width, scene_height, scene_images = 0, 0, []
        for scene_image_path in scene_image_paths:
            image, boxes = read_scene(image_path=scene_image_path)
            drawn_image = draw_boxes(canvas=image,
                                     boxes=boxes)
            scene_width += drawn_image.width
            scene_height = max(scene_height, drawn_image.height)
            scene_images.append(drawn_image)

        scene = Image.new(mode='RGB', size=(scene_width, scene_height), color=BACKGROUND_COLOR)
        start_x = 0
        for scene_image in scene_images:
            scene.paste(scene_image, (start_x, 0))
            start_x += scene_image.width

        cv2.imshow(f"Scene {scene_no_str}", cv2.cvtColor(np.array(scene), cv2.COLOR_RGB2BGR))
        cv2.waitKey(0)
        cv2.destroyWindow(f"Scene {scene_no_str}")
