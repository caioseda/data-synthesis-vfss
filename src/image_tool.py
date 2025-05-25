from PIL import Image
import cv2 as cv
import logging
from .utils import get_video_path_from_id

def save_image(img, output_path, log=False):
    """
    Save an image to the specified output path.

    Parameters:
        img (numpy.ndarray): The image to save.
        output_path (str): The path where the image will be saved.
        log (bool): Whether to log the saving action.

    Returns:
        None
    """
    if log:
        logging.info(f"Saving image to {output_path}")
    
    # Ensure the output directory exists
    image = Image.fromarray(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    image.save(output_path)
    

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
