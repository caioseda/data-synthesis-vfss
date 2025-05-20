import cv2 as cv
import numpy as np
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


def play_video(video_id, video_dir='data/videos/', start_frame=0, end_frame=None):
    """
    Play a video from a specified start frame to an end frame.
    The video can be paused and navigated frame by frame using the arrow keys.
    Press 'q' to quit the video.
    Press 'space' to pause/play the video.
    Press 'right arrow' to go to the next frame.
    Press 'left arrow' to go to the previous frame.

    Parameters:
        video_id (str): The ID of the video to play.
        video_dir (str): The directory where the videos are stored.
        start_frame (int): Frame number to start playing the video from.
        end_frame (int): Frame number to stop playing the video at. If None, plays until the end of the video.

    Returns:
        None
    """
    # Get the video path
    video_path = get_video_path_from_id(video_id, video_dir)

    # Load the video
    cap = cv.VideoCapture(video_path)
    
    # Check if video loaded successfully
    if not cap.isOpened():
        logging.error("Error: Could not open video.")
        exit()

    # Check if end_frame is valid
    total_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    if end_frame is None:
        end_frame = total_frames
    elif end_frame > total_frames:
        end_frame = total_frames
    
    # Check if start_frame is valid
    if start_frame > 0:
        frame_idx = start_frame
    
    if start_frame >= end_frame:
        logging.error("Error: start_frame must be less than end_frame.")
        exit()

    # Frame index
    frame_idx = 0
    paused = False
    while True:
        key = cv.waitKey(30)

        if key == ord('q'):  # Quit
            break
        elif key == 32:  # Spacebar toggles pause/play
            paused = not paused
        elif paused and (key == 3 or key == 2555904):  # Right Arrow (next frame)
            if frame_idx < total_frames - 1:
                frame_idx += 1
                paused = True
        elif paused and (key == 2 or key == 2424832):  # Left Arrow (previous frame)
            if frame_idx > 0:
                frame_idx -= 1
                paused = True

        if paused:
            if key != -1:
                print("Paused at frame: " + str(frame_idx))
                print("The key code is:"+str(key))
        
        # if not paused, play the video normally
        if not paused:
            frame_idx += 1

        if frame_idx < end_frame:
            # Set next frame position
            cap.set(cv.CAP_PROP_POS_FRAMES, frame_idx)
            # Read the next frame and display it
            ret, frame = cap.read()
            cv.imshow("Video", frame)
        else: 
            # If we reach the end of the video, break the loop
            break

    cap.release()
    cv.destroyAllWindows()

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
        
def save_frame_as_image(frame, output_path, log=False):
    """
    Save a video frame as an image.

    Parameters:
        frame (numpy.ndarray): The frame to save.
        output_path (str): Path to save the image.
        log (bool): Whether to log the saving process.

    Returns:
        None
    """
    if log:
        logging.info(f"Saving frame to {output_path}")
    
    cv.imwrite(output_path, frame)
