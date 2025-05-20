import logging

from src.utils import get_video_path_from_id
from src.media_player import play_video
from src.video_labels import read_video_labels_df 
from src.create_dataset import create_max_constriction_dataset

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Process some integers.")

    parser.add_argument('--video_dir', type=str, default='data/videos/', help='Path to the video directory')
    parser.add_argument('--labels', type=str, default='data/rotulos/Frames e PAS.xlsx', help='Path to the labels file')
    parser.add_argument('--video_id', type=str, default='1', help='ID of the video to play')
    parser.add_argument('--output_dir', type=str, default='data/images/max_constriction/', help='Path to the output directory for images')
    parser.add_argument('--frame_size', type=tuple, default=(512, 512), help='Size of the output images (width, height)')
    return parser.parse_args()

if __name__ == "__main__":
    # Parse command line arguments
    args = parse_args()
    
    # Read the rotulos DataFrame
    df_frames_pas = read_video_labels_df(args.labels)
    logging.info("Labels dataframe loaded successfully.")

    # Create a dataset of images from the maximum constriction frames of videos
    create_max_constriction_dataset(
        df_labels = df_frames_pas,
        video_dir = args.video_dir,
        output_dir = args.output_dir,
        frame_size = args.frame_size
    )
    logging.info("Max constriction dataset created successfully.")

    # play_video(
    #     video_id=args.video_id,
    #     video_dir=args.video_dir,
    #     start_frame=0,
    #     end_frame=None
    # )
    
    