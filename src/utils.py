import logging
import os

def get_video_path_from_id(video_id, video_dir='data/videos/'):
    """
    Get the full path of a video file given its ID.

    Parameters:
        video_id (str): The ID of the video.
        video_dir (str): The directory where the videos are stored.

    Returns:
        str: The full path to the video file.
    """
    video_path = f"{video_dir}{video_id}.avi"
    if not os.path.exists(video_path):
        logging.error(f"Error: Video file {video_path} does not exist.")
        exit()
    return video_path