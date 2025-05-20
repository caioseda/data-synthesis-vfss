import cv2 as cv
import numpy as np
import logging

def show_video_frame(video_path, frame_number):
    """
    Display a specific frame from a video.
    """
    cap = cv.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # Set the frame position
    cap.set(cv.CAP_PROP_POS_FRAMES, frame_number)

    ret, frame = cap.read()
    if ret:
        cv.imshow('Frame', frame)
        cv.waitKey(0)
        cv.destroyAllWindows()
    else:
        print("Error: Could not read frame.")
    
    cap.release()

def play_video(video_path, start_frame=0, end_frame=None):
    """
    Play a video from a specified start frame to an end frame.
    The video can be paused and navigated frame by frame using the arrow keys.
    Press 'q' to quit the video.
    Press 'space' to pause/play the video.
    Press 'right arrow' to go to the next frame.
    Press 'left arrow' to go to the previous frame.

    Parameters:
        video_path (str): Path to the video file.
        start_frame (int): Frame number to start playing the video from.
        end_frame (int): Frame number to stop playing the video at. If None, plays until the end of the video.

    Returns:
        None
    """
    # Load the video
    cap = cv.VideoCapture(video_path)
    
    # Check if video loaded successfully
    if not cap.isOpened():
        logging.error("Error: Could not open video.")
        exit()

    # Read total number of frames
    total_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))

    # Check if end_frame is valid
    if start_frame > 0:
        frame_idx = start_frame
    if end_frame is not None and end_frame > total_frames:

        end_frame = total_frames
    if end_frame is not None and start_frame >= end_frame:
        logging.error("Error: start_frame must be less than end_frame.")
        exit()

    # Frame index
    frame_idx = 0
    paused = False

    while True:
        if end_frame is not None and frame_idx >= end_frame:
            break
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
        
        # Set next frame position
        cap.set(cv.CAP_PROP_POS_FRAMES, frame_idx)
        
        # Read the next frame and display it
        ret, frame = cap.read()
        cv.imshow("Video", frame)

    cap.release()
    cv.destroyAllWindows()

    def get_video_frame(video_path, frame_number):
        """
        Get a specific frame from a video.

        Parameters:
            video_path (str): Path to the video file.
            frame_number (int): Frame number to extract.

        Returns:
            frame (numpy.ndarray): The extracted frame as a numpy array.
        """
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
