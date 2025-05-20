import cv2 as cv
import pandas as pd
import os
import numpy as np
import logging

from src.media_player import play_video
from src.video_labels import read_video_labels_df 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Process some integers.")

    parser.add_argument('--video', type=str, default='data/videos/', help='Path to the video directory')
    parser.add_argument('--labels', type=str, default='data/rotulos/Frames e PAS.xlsx', help='Path to the labels file')
    parser.add_argument('--video_id', type=str, default='1', help='ID of the video to play')
    return parser.parse_args()

if __name__ == "__main__":
    # Parse command line arguments
    args = parse_args()
    # Get the video path from the command line arguments
    # Read the rotulos DataFrame
    df_frames_pas = read_video_labels_df(args.labels)
    
    print(df_frames_pas)
    play_video(
        1,
        video_dir=args.video,
        start_frame=0,
        end_frame=None
    )
    
    