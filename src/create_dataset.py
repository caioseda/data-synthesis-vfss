import os
from .video_tool import get_video_frame
from .image_tool import save_image
from .utils import get_video_path_from_id
import cv2 as cv
import logging

# Logging configuration
logging.getLogger()

def create_max_constriction_dataset(df_labels, video_dir, dataset_dir, frame_size=(512, 512)):
    """
    Create a dataset of images from the maximum constriction frames of videos.

    Parameters:
        df_labels (pd.DataFrame): DataFrame containing video labels.
        video_dir (str): Directory where the videos are stored.
        dataset_dir (str): Directory where the images will be saved.

    Returns:
        None
    """
    # Ensure the output directory exists
    os.makedirs(dataset_dir, exist_ok=True)

    rescaled_videos_id = []
    for _, row in df_labels.iterrows():
        video_id = row['video_id']
        frame_number = row['frame_max_constricao']
        
        # Get the video path
        video_path = get_video_path_from_id(video_id, video_dir)
        
        # Get the frame
        frame = get_video_frame(video_id, frame_number, video_dir)
        
        if frame is not None:
            # Resize the frame if necessary
            if (frame.shape[1], frame.shape[0]) != frame_size:
                frame = cv.resize(frame, frame_size)
                rescaled_videos_id.append(row.video_id)

            # Save the frame as an image
            output_path = os.path.join(dataset_dir, f"{video_id}_max_constriction.png")
            save_image(frame, output_path)

        else:
            logging.error(f"Frame not found for video ID: {video_id} at frame number: {frame_number}")

    logging.info(f"{len(rescaled_videos_id)} videos needed to be resized to {frame_size[0]}x{frame_size[1]}: {rescaled_videos_id}")

def create_all_frames_dataset(videos_dir, dataset_dir, frame_size=(512, 512)):
    """
    Create a dataset of all frames from videos.

    Parameters:
        videos_dir (str): Directory where the videos are stored.
        dataset_dir (str): Directory where the images will be saved.

    Returns:
        None
    """
    os.makedirs(dataset_dir, exist_ok=True)
    video_files = [f for f in os.listdir(videos_dir) if f.endswith('.avi')]

    for video_file in video_files:
        videos_id = os.path.splitext(video_file)[0]
        video_path = os.path.join(videos_dir, video_file)
        cap = cv.VideoCapture(video_path)
        if not cap.isOpened():
            logging.error(f"Error: Could not open video {video_path}.")
            continue
        
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Resize the frame if necessary
            if (frame.shape[1], frame.shape[0]) != frame_size:
                frame = cv.resize(frame, frame_size)

            # Save the frame as an image
            output_path = os.path.join(dataset_dir, f"{videos_id}_frame_{frame_count}.png")
            save_image(frame, output_path)
            frame_count += 1
        
        cap.release()
    logging.info(f"All frames from videos in {videos_dir} have been saved to {dataset_dir}.")

