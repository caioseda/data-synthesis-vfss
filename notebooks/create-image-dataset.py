import cv2 as cv
import pandas as pd
import os
import numpy as np
import logging

from src.media_player import play_video
from src.video_labels import read_video_labels_df 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    # Define the path to the Excel file
    path = 'data/rotulos/Frames e PAS.xlsx'
    
    # Read the rotulos DataFrame
    df_frames_pas = read_video_labels_df(path)
    print(df_frames_pas.head())
    play_video('data/videos/1.avi')
    
    