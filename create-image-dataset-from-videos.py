import logging
import os
import argparse
from src.video_labels import read_video_labels_df 
from src.create_dataset import create_max_constriction_dataset, create_all_frames_dataset
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def create_dataset_dir(args):
    """
    Create a directory for the dataset based on the current run ID and dataset type.
    """
    dataset_type = args.dataset_type
    dataset_type = dataset_type.replace('_', '-')

    prev_run_dirs = []
    if os.path.isdir(args.output_dir):
        prev_run_dirs = [
            d 
            for d in os.listdir(args.output_dir) 
            if os.path.isdir(os.path.join(args.output_dir, d))
            and dataset_type in d
        ]
        prev_run_ids = [re.match(r'^\d+', d) for d in prev_run_dirs]
        prev_run_ids = [int(d.group(0)) for d in prev_run_ids if d is not None]
        cur_run_id = max(prev_run_ids, default=-1) + 1

    dataset_dir = f'{cur_run_id:05d}-{dataset_type}-{args.frame_size[0]}'
    dataset_dir = os.path.join(args.output_dir, dataset_dir)

    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir)
        logging.info(f"Created directory: {dataset_dir}")
    else:
        logging.warning(f"Directory {dataset_dir} already exists. Please choose a different name or remove the existing directory.")
    
    return dataset_dir



def parse_args():
    parser = argparse.ArgumentParser(description="Process some integers.")

    parser.add_argument('--video-dir', type=str, default='data/videos/', help='Path to the video directory')
    parser.add_argument('--labels', type=str, default='data/rotulos/Frames e PAS.xlsx', help='Path to the labels file')
    parser.add_argument('--output-dir', type=str, default='data/images/', help='Path to the output directory for images')
    parser.add_argument('--frame-size', type=tuple, default=(512, 512), help='Size of the output images (width, height)')
    parser.add_argument('--dataset-type', type=str, default='max_constriction', choices=['max_constriction', 'all_frames'], help='Type of dataset to create: max_constriction or all_frames')
    parser.add_argument('--dry-run', action='store_true', help='If set, only create the dataset directory without processing videos')
    
    args = parser.parse_args()

    # Validating the arguments
    if args.dataset_type not in ['max_constriction', 'all_frames']:
        parser.error("Invalid dataset type. Choose 'max_constriction' or 'all_frames'.")

    if not os.path.isdir(args.output_dir):
        os.makedirs(args.output_dir)
        logging.info(f"Created output directory: {args.output_dir}")
    
    if not os.path.isdir(args.video_dir):
        parser.error(f"Video directory {args.video_dir} does not exist.")

    if not os.path.isfile(args.labels):
        parser.error(f"Labels file {args.labels} does not exist.")
        
    args.dataset_dir = create_dataset_dir(args)

    return args

if __name__ == "__main__":
    # Parse command line arguments
    args = parse_args()

    if args.dry_run:
        logging.info("Dry run mode. Only creating the dataset directory.")
        exit(0)

    # Create a dataset of images from the maximum constriction frames of videos
    if args.dataset_type == 'all_frames':
        create_all_frames_dataset(
            videos_dir = args.video_dir,
            dataset_dir = args.dataset_dir,
            frame_size = args.frame_size
        )
        logging.info("All frames dataset created successfully.")
    else:
        # Read the rotulos DataFrame
        df_frames_pas = read_video_labels_df(args.labels)
        logging.info("Labels dataframe loaded successfully.")

        # Create a dataset of images from the maximum constriction frames of videos
        create_max_constriction_dataset(
            df_labels = df_frames_pas,
            video_dir = args.video_dir,
            dataset_dir = args.dataset_dir,
            frame_size = args.frame_size
        )
    logging.info("Max constriction dataset created successfully.")
    
    