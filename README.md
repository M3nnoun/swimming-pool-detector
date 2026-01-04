# Pool Detector – Swimming Pool Detection in Aerial Images

A Python CLI tool that detects swimming pools in aerial/satellite images using **image processing** techniques (OpenCV + HSV color segmentation + morphological operations).

The tool supports detection of **multiple pools** per image (rectangular, oval and some irregular shapes).  
Outputs:
- Text file with boundary coordinates of all detected pools
- Annotated image with red outlines around each pool

→ For **significantly better performance** (especially on difficult/irregular pools), check out the separate deep learning notebook (hosted on Google Colab).  
The model used there is quite large (~3.2 GB), which is why it isn't included in this lightweight CLI tool.

🔗 **Better performing version (Deep Learning notebook):**  
https://colab.research.google.com/drive/1rONpM9Q0DIvw5DhLNd4W54a4nrwUNDu9?usp=sharing

## Features

- Detects multiple pools in the same image
- Works with rectangular, oval and some irregular pool shapes
- Clean modular structure (detector, utils, CLI entrypoint)
- Configurable parameters (color thresholds, min area, outline thickness…)
- Very lightweight – no large models or external APIs required

## Project Structure

```
pool_detector/
├── src/
│   ├── cli.py                  # Main CLI entry point
│   ├── detectors/
│   │   ├── base.py
│   │   └── opencv_detector.py  # HSV + morphology based detector
│   └── utils/
│       ├── image.py            # Image loading & drawing
│       └── output.py           # Coordinate saving
├── data/
│   ├── input/                  # Put your test aerial images here
│   └── output/                 # Generated results (auto-created)
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.10+
- Virtual environment (strongly recommended)

### Dependencies

```bash
opencv-python
numpy
pillow
```

## Installation

```bash
# 1. Go to project folder
cd pool_detector

# 2. Create & activate virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
# or manually:
pip install opencv-python numpy pillow
```

## Usage

```bash
# Basic usage
python src/cli.py data/input/your_image.jpg

# Custom options
python src/cli.py data/input/000000079.jpg --thickness 2 --output-dir data/output/
```

### Available Arguments

| Flag              | Description                               | Default      |
|-------------------|-------------------------------------------|--------------|
| `image`           | Path to input aerial image                | (required)   |
| `--thickness`     | Outline thickness in pixels               | `1`          |
| `--output-dir` / `-o` | Where to save results                 | `data/output`|

### Output Files (example for `image.jpg`)

```
data/output/
├── image_coords.txt           # All detected pools coordinates
└── image_result.jpg           # Original image + red outlines
```

**Example content of coordinates file:**

```
Detected Swimming Pool Boundary Coordinates
==========================================

--- Pool 1 (22 points) ---
145, 278
189, 265
...

--- Pool 2 (16 points) ---
512, 340
...
```

## Tips for Better Detection

- **Tuning HSV range** → edit `opencv_detector.py` (current: hue 80–135)
- **Small pools not detected?** → decrease `min_pool_area` / `min_area_ratio`
- **Too many false positives?** → increase thresholds or add more aggressive morphology
- **Still not satisfied?** → Try the deep learning notebook linked above — it usually gives much better results on challenging images

---

Made with ❤️ for the SanadTech technical test – 2026
