from src.utils import get_video_path_from_id
from src.video_tool import convert_avi_to_mp4
import logging
import argparse
import cv2 as cv


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def write_text(frame, text, pos, font=cv.FONT_HERSHEY_SIMPLEX, font_scale=0.6, color=(0, 255, 0), thickness=2):
    """
    Writes a given text on the frame at the specified position.
    
    Parameters:
        frame (ndarray): The current video frame.
        text (str): The text to overlay.
        pos (tuple): The (x, y) coordinates for the text.
        font (int): OpenCV font type.
        font_scale (float): Scale factor for the text size.
        color (tuple): Color of the text in BGR.
        thickness (int): Thickness of the text.
    
    Returns:
        The frame with the text overlay.
    """
    cv.putText(frame, text, pos, font, font_scale, color, thickness)
    return frame

def write_frame_number(frame, frame_idx, total_frames):
    """
    Overlays the frame number on the top right of the frame.
    
    Parameters:
        frame (ndarray): The current video frame.
        frame_idx (int): The current frame index.
    
    Returns:
        The frame with the frame number overlay.
    """
    text = f"Frame: {frame_idx:03d} / {total_frames:03d}"
    (text_width, text_height), _ = cv.getTextSize(text, cv.FONT_HERSHEY_SIMPLEX, 1, 2)
    x_pos = 10
    y_pos = 70
    return write_text(frame, text, (x_pos, y_pos))

def write_time_info(frame, frame_idx, fps, total_minutes, total_seconds):
    """
    Overlays the current time and total duration on the top left of the frame.
    
    Parameters:
        frame (ndarray): The current video frame.
        frame_idx (int): The current frame index.
        fps (float): Frames per second of the video.
        total_minutes (int): Total minutes of the video.
        total_seconds (int): Total seconds (remaining after minutes) of the video.
    
    Returns:
        The frame with the time info overlay.
    """
    current_time = frame_idx / fps
    current_minutes = int(current_time // 60)
    current_seconds = int(current_time % 60)
    text = f"{current_minutes}m {current_seconds:02d}s / {total_minutes}m {total_seconds:02d}s"
    x_pos = 10
    y_pos = 30
    return write_text(frame, text, (x_pos, y_pos))

def write_autoclose_info(frame, autoclose):
    """
    Overlays the autoclose status on the bottom left of the frame.
    
    Parameters:
        frame (ndarray): The current video frame.
        autoclose (bool): Whether autoclose is enabled or not.
    
    Returns:
        The frame with the autoclose info overlay.
    """
    text = "Autoclose: " + ("ON" if autoclose else "OFF")
    x_pos = 10
    y_pos = frame.shape[0] - 10
    return write_text(frame, text, (x_pos, y_pos))

def write_pause_info(frame, paused):
    """
    Overlays the pause status on the bottom right of the frame.
    
    Parameters:
        frame (ndarray): The current video frame.
        paused (bool): Whether the video is paused or not.
    
    Returns:
        The frame with the pause info overlay.
    """
    text = "Paused" if paused else "Playing"
    x_pos = frame.shape[1] - 100
    y_pos = frame.shape[0] - 10
    return write_text(frame, text, (x_pos, y_pos))

def play_video(video_id, video_dir='data/videos/', start_frame=0, end_frame=None, paused=False, show_info=True, autoclose=True):
    """
    Play a video from a specified start frame to an end frame.
    The video can be paused and navigated frame by frame using the arrow keys.
    Press 'q' to quit the video.
    Press 'space' to pause/play the video.
    Press 'right arrow' to go to the next frame.
    Press 'left arrow' to go to the previous frame.
    Press 'i' to toggle the time and frame number displays.
    Press 'a' to toggle the autoclose behavior when the video finishes.

    Parameters:
        video_id (str): The ID of the video to play.
        video_dir (str): The directory where the videos are stored.
        start_frame (int): Frame number to start playing the video from.
        end_frame (int): Frame number to stop playing the video at. If None, plays until the end of the video.
        paused (bool): Whether to start the video in a paused state.
        show_info (bool): Whether to overlay time and frame info on the video.
        autoclose (bool): Whether to automatically close the video window when finished.

    Returns:
        None
    """
    video_path = get_video_path_from_id(video_id, video_dir)
    cap = cv.VideoCapture(video_path)

    if not cap.isOpened():
        logging.error("Error: Could not open video.")
        exit()

    fps = cap.get(cv.CAP_PROP_FPS)
    total_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))

    if end_frame is None or end_frame > total_frames:
        end_frame = total_frames

    if start_frame >= end_frame:
        logging.error("Error: start_frame must be less than end_frame.")
        exit()

    frame_idx = start_frame
    cap.set(cv.CAP_PROP_POS_FRAMES, frame_idx)

    total_time = total_frames / fps
    total_minutes = int(total_time // 60)
    total_seconds = int(total_time % 60)

    while True:
        delay = int(1000 / fps) if not paused else 30
        key = cv.waitKey(delay)

        if key == ord('q'):
            break
        elif key == ord(' '):
            paused = not paused
        elif key == ord('i'):
            show_info = not show_info
        elif key == ord('a'):
            autoclose = not autoclose
            print("Autoclose toggled", "ON" if autoclose else "OFF")
        elif key == ord('e'):
            output_path = video_path.replace('.avi', '.mp4')
            convert_avi_to_mp4(video_path, output_path)
        elif paused and (key == 3 or key == 2555904):  # Right Arrow
            if frame_idx < total_frames - 1:
                frame_idx += 1
        elif paused and (key == 2 or key == 2424832):  # Left Arrow
            if frame_idx > 0:
                frame_idx -= 1

        # Auto-advance only when not paused
        if not paused:
            if frame_idx < end_frame - 1:
                frame_idx += 1
            else:
                # If we're at the end and autoclose is enabled, exit.
                if autoclose:
                    break
                else: # Otherwise, remain on the last available frame.
                    paused = True

        cap.set(cv.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret:
            break
        if show_info:
            frame = write_frame_number(frame, frame_idx, total_frames-1)
            frame = write_time_info(frame, frame_idx, fps, total_minutes, total_seconds)
            frame = write_autoclose_info(frame, autoclose)
            frame = write_pause_info(frame, paused)

        cv.imshow("Video", frame)

    cap.release()
    cv.destroyAllWindows()

def parse_args():
    parser = argparse.ArgumentParser(description="Play a video with frame navigation.")
    parser.add_argument('-s', '--video_id', type=str, required=True, help='ID of the video to play')
    parser.add_argument('--video_dir', type=str, default='data/videos/', help='Path to the video directory')
    parser.add_argument('-st','--start_frame', type=int, default=0, help='Frame number to start playing the video from')
    parser.add_argument('-e','--end_frame', type=int, default=None, help='Frame number to stop playing the video at')
    parser.add_argument('--paused', action='store_true', default=False, help='Start the video in paused state')
    parser.add_argument('--show_info', action='store_true', default=True, help='Show time and frame number info')
    parser.add_argument('--no_autoclose', action='store_true', help='Disable auto-closing the video window when finished playing')
    
    return parser.parse_args()
    
if __name__ == "__main__":
    args = parse_args()
    
    # Determine autoclose from the command line flag
    autoclose = not args.no_autoclose

    # Print commands for user
    print("Press 'q' to quit the video.")
    print("Press 'space' to pause/play the video.")
    print("Press 'right arrow' to go to the next frame.")
    print("Press 'left arrow' to go to the previous frame.")
    print("Press 'i' to toggle the time and frame number displays.")
    print("Press 'a' to toggle the autoclose behavior.")
    logging.info("Starting video playback...")

    play_video(
        video_id=args.video_id,
        video_dir=args.video_dir,
        start_frame=args.start_frame,
        end_frame=args.end_frame,
        paused=args.paused,
        show_info=args.show_info,
        autoclose=autoclose
    )
    logging.info("Video played successfully.")