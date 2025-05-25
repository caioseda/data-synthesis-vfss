from src.utils import get_video_path_from_id
import logging
import argparse
import cv2 as cv

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

def parse_args():
    parser = argparse.ArgumentParser(description="Play a video with frame navigation.")
    parser.add_argument('-s', '--video_id', type=str, required=True, help='ID of the video to play')
    parser.add_argument('--video_dir', type=str, default='data/videos/', help='Path to the video directory')
    parser.add_argument('--start_frame', type=int, default=0, help='Frame number to start playing the video from')
    parser.add_argument('--end_frame', type=int, default=None, help='Frame number to stop playing the video at')
    return parser.parse_args()
    
if __name__ == "__main__":
    # Parse command line arguments
    args = parse_args()
    
    # Play the video
    play_video(
        video_id=args.video_id,
        video_dir=args.video_dir,
        start_frame=args.start_frame,
        end_frame=args.end_frame
    )
    logging.info("Video played successfully.")