# Synthesizing VFSS Data Using StyleGAN2-ADA: A Generative Approach for Swallowing Disorder Research

## Overview
This project focuses on synthesizing VFSS (Videofluoroscopic Swallowing Study) data using StyleGAN2-ADA. The goal is to create a dataset that can be used for research in swallowing disorders. 
The project includes various scripts and notebooks for data processing, model training, and evaluation.
We also provide tools like: 
- `media_player.py`: A simple media player for playing videos.
- `create-image-dataset-from-videos.py`: A script to create an image dataset from videos.

## Directory Structure
```
├── data
│   ├── videos
│   ├── images
│   ├── labels
│   └── ...
├── notebooks
│   ├── applying-stylegan-on-vfss.ipynb
│   └── create-image-dataset.ipynb
├── src
│   ├── video_tool.py
│   ├── image_tool.py
│   ├── utils.py
│   ├── create_dataset.py
│   ├── video_labels.py
│   └── ...
├── README.md
├── create-image-dataset-from-videos.py
├── media_player.py
└── environment.yml
```

## Requirements
- Python 3.12.2 or higher
- OpenCV
- Pandas
- NumPy
  
## Installation
1. Clone the repository:
   ```bash
   git clone  https://github.com/caioseda/data-synthesis-vfss.git
   ```
2. Navigate to the project directory:
   ```bash
   cd data-synthesis-vfss
   ```
3. Install the required packages:
   ```bash
   conda env create -f environment.yml
   conda activate vfss
   ```

## Usage
### Playing Videos
To play a video, use the `media_player.py` script. You can specify the video_dir, video ID, start frame, and end frame.
You can navigate through the video using the arrow keys and pause/play using the spacebar. Use 'q' to quit the video.
You can also toggle the display of time and frame number using 'i' and toggle the autoclose behavior using 'a'.

```bash
python media_player.py \
   --video_dir data/videos/ \
   --video_id 1 
```

### Creating Image Dataset from Videos
To create an image dataset from videos, use the `create-image-dataset-from-videos.py` script.
You can specify the video directory, labels file, video ID, output directory, frame size, and dataset type (max_constriction or all_frames).

```bash
python create-image-dataset-from-videos.py \
  --video-dir data/videos/ \
  --labels data/rotulos/Frames e PAS.xlsx \
  --video-id 1 --output-dir data/images/ \
  --frame-size (512, 512) \
  --dataset-type all_frames
```

## Acknowledgements
- [StyleGAN3](https://github.com/NVlabs/stylegan3) implementation

