import numpy as np
import cv2

def load_image(path: str) -> cv2.typing.MatLike:
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Cannot load image: {path}")
    return img

def draw_polygons(image, polygons_list: list[list[tuple[int,int]]], 
                  color=(0, 0, 255), thickness=2, line_type=cv2.LINE_AA):
    """
    Draw outlines for ALL detected pools (multiple polygons)
    """
    if not polygons_list:
        return
    
    for polygon in polygons_list:
        if len(polygon) < 3:
            continue
        pts = np.array(polygon, dtype=np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(image, [pts], isClosed=True, 
                      color=color, thickness=thickness, lineType=line_type)