# Pool Detector – Swimming Pool Detection in Aerial Images

A Python CLI tool that detects swimming pools in aerial/satellite images using two approaches:

- **Traditional Computer Vision** (OpenCV + HSV color segmentation)  
- **Multimodal LLM** (Google Gemini API)  

Supports detection of **multiple pools** per image. Outputs:
- Text file with boundary coordinates of all detected pools
- Annotated image with red outlines around each pool

## Features

- Detects rectangular, oval, and irregular shaped pools
- Handles multiple pools in the same image
- Clean modular structure (detectors, utils, CLI entrypoint)
- Easy to switch between CV and LLM methods
- Configurable parameters (thresholds, thickness, etc.)

## Project Structure

```
pool_detector/
├── src/
│   ├── cli.py                  # Main CLI entry point
│   ├── detectors/
│   │   ├── base.py
│   │   ├── opencv_detector.py  # HSV + morphology based detector
│   │   └── llm_detector.py     # Google Gemini vision model
│   └── utils/
│       ├── image.py            # Image loading & drawing
│       └── output.py           # Coordinate saving
├── data/
│   ├── input/                  # Put your test aerial images here
│   └── output/                 # Generated results (auto-created)
├── .env                        # API keys (GEMINI_API_KEY=...)
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
python-dotenv
google-genai
```

## Installation

```bash
# 1. Clone or go to project folder
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
pip install opencv-python numpy pillow python-dotenv google-genai

# 4. Create .env file in root folder (for LLM method)
# Example:
# GEMINI_API_KEY=your_api_key_here
# Get your key: https://aistudio.google.com/app/apikey
```

## Usage

```bash
# Basic usage (default: opencv method)
python src/cli.py data/input/your_image.jpg

# Specify method
python src/cli.py data/input/000000079.jpg --method opencv
python src/cli.py data/input/000000079.jpg --method llm

# Custom output folder + thin outline
python src/cli.py data/input/image.jpg \
  --method opencv \
  --thickness 1 \
  --output-dir results/today/
```

### Available Arguments

| Flag              | Description                               | Default      |
|-------------------|-------------------------------------------|--------------|
| `image`           | Path to input aerial image                | (required)   |
| `--method` / `-m` | Detection method                          | `opencv`     |
| `--thickness`     | Outline thickness in pixels               | `1`          |
| `--output-dir` / `-o` | Where to save results                  | `data/output`|

### Output Files (example for `image.jpg`)

```
data/output/
├── image_coords_opencv.txt     # All detected pools coordinates
└── image_result_opencv.jpg     # Original + red outlines
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

## Tips for Better Detection (OpenCV)

- **Tuning HSV range** → edit `opencv_detector.py` (current: hue 80–135)
- **Small pools not detected?** → decrease `min_pool_area` / `min_area_ratio`
- **Too many false positives?** → increase thresholds or add more morphology

## LLM Method Notes

- Requires valid `GEMINI_API_KEY` in `.env`
- Uses latest Google Gemini model (vision-capable)
- Slower and more expensive than OpenCV, but better for irregular shapes
- Prompt is in `llm_detector.py` — feel free to improve it

## Future Improvements (Nice-to-have)

- Add support for more LLM providers (Claude, GPT-4o, Grok)
- Fine-tune segmentation model (SAM / U-Net)
- Add confidence scores
- Batch processing mode

## License

MIT License — feel free to use for your portfolio or projects!

Made with ❤️ for the SanadTech technical test – 2026