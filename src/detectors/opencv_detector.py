import cv2
import numpy as np
from typing import List, Tuple
from .base import PoolDetector

class OpenCvDetector(PoolDetector):
    """
    Detects ALL swimming pools using HSV color segmentation + morphology
    Returns list of polygons (each polygon = list of (x,y) points)
    """
    def __init__(
        self,
        min_pool_area: int = 600,              
        min_area_ratio: float = 0.0015,        
        hsv_lower = np.array([80, 50, 40]),
        hsv_upper = np.array([135, 255, 255]),
        morph_kernel_size: int = 5
    ):
        self.min_pool_area = min_pool_area
        self.min_area_ratio = min_area_ratio
        self.hsv_lower = hsv_lower
        self.hsv_upper = hsv_upper
        self.kernel = np.ones((morph_kernel_size, morph_kernel_size), np.uint8)

    def detect(self, image_path: str) -> List[List[Tuple[int, int]]]:
        """
        Returns:
            list of polygons, where each polygon is list of (x,y) points
            Empty list if no pools found
        """
        img = cv2.imread(image_path)
        if img is None:
            print(f"Failed to load image: {image_path}")
            return []

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.hsv_lower, self.hsv_upper)

        # Clean mask
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN,  self.kernel, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, self.kernel, iterations=3)

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            return []

        image_area = img.shape[0] * img.shape[1]
        detected_polygons = []

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < self.min_pool_area:
                continue
            if area < self.min_area_ratio * image_area:
                continue

            # Approximate polygon (smooth)
            epsilon = 0.008 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, closed=True)

            # Convert to list of tuples
            points = approx.reshape(-1, 2)
            polygon = [(int(x), int(y)) for x, y in points]

            # Ensure closed polygon
            if len(polygon) >= 3 and polygon[0] != polygon[-1]:
                polygon.append(polygon[0])

            detected_polygons.append(polygon)

        return detected_polygons