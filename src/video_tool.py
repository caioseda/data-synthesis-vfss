from .utils import get_video_path_from_id
import cv2 as cv
from PIL import Image
import logging

def get_video_frame(video_id, frame_number, video_dir='data/videos/'):
    """
    Get a specific frame from a video.

    Parameters:
        video_id (str): The ID of the video.
        frame_number (int): Frame number to extract.
        video_dir (str): The directory where the videos are stored.

    Returns:
        frame (numpy.ndarray): The extracted frame as a numpy array.
    """
    # Get the video path
    video_path = get_video_path_from_id(video_id, video_dir)
    
    # Load the video
    cap = cv.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Could not open video.")
        return None

    # Set the frame position
    cap.set(cv.CAP_PROP_POS_FRAMES, frame_number)

    ret, frame = cap.read()
    if ret:
        return frame
    else:
        print("Error: Could not read frame.")
        return None
    
def get_all_frames(video_id, video_dir='data/videos/'):
    """
    Get all frames from a video.

    Parameters:
        video_id (str): The ID of the video.
        video_dir (str): The directory where the videos are stored.

    Returns:
        frames (list): A list of frames as numpy arrays.
    """
    # Get the video path
    video_path = get_video_path_from_id(video_id, video_dir)
    
    # Load the video
    cap = cv.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Could not open video.")
        return None

    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    
    return frames

def save_frames_as_video(frames, output_path, fps=30):
    """
    Save a list of frames as a video file.

    Parameters:
        frames (list): List of frames as numpy arrays.
        output_path (str): Path to save the output video.
        fps (int): Frames per second for the video.
    """
    if not frames:
        logging.error("No frames to save.")
        return

    height, width, layers = frames[0].shape
    fourcc = cv.VideoWriter_fourcc(*'mp4v')  # Codec for mp4
    video_writer = cv.VideoWriter(output_path, fourcc, fps, (width, height))

    for frame in frames:
        video_writer.write(frame)

    video_writer.release()
    logging.info(f"Video saved as {output_path}")


