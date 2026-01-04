import argparse
from pathlib import Path

from detectors.opencv_detector import OpenCvDetector
from utils.image import load_image, draw_polygons
from utils.output import save_coordinates
import cv2

DETECTORS = {
    "opencv": OpenCvDetector
}

def main():
    parser = argparse.ArgumentParser(description="Swimming pool detector")
    parser.add_argument("image", type=str, help="input image path")
    parser.add_argument("-m", "--method", choices=["opencv"], default="opencv",
                        help="detection method")
    parser.add_argument("-o", "--output-dir", type=str, default="./data/output",
                        help="where to save results")

    args = parser.parse_args()

    input_path = Path(args.image)
    if not input_path.is_file():
        print(f"Image not found: {input_path}")
        return 1

    detector_class = DETECTORS.get(args.method)
    print(f"Using detector: {args.method}")
    detector = detector_class()

    coordinates = detector.detect(str(input_path))

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    stem = input_path.stem
    coord_path = output_dir / f"{stem}_coords_{args.method}.txt"
    image_path = output_dir / f"{stem}_result_{args.method}.jpg"

    save_coordinates(coordinates, coord_path)

    if coordinates:
        img = load_image(str(input_path))
        draw_polygons(img, coordinates, color=(0, 0, 255), thickness=1)
        cv2.imwrite(str(image_path), img)
        print(f"Results saved:")
        print(f"  Coordinates → {coord_path}")
        print(f"  Image       → {image_path}")
    else:
        print("No pool detected.")

    return 0


if __name__ == "__main__":
    exit(main())
