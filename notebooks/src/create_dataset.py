import os
from .media_player import get_video_frame, save_frame_as_image
from .utils import get_video_path_from_id

def create_max_constriction_dataset(df_labels, video_dir, output_dir):
    """
    Create a dataset of images from the maximum constriction frames of videos.

    Parameters:
        df_labels (pd.DataFrame): DataFrame containing video labels.
        video_dir (str): Directory where the videos are stored.
        output_dir (str): Directory where the images will be saved.

    Returns:
        None
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    for _, row in df_labels.iterrows():
        video_id = row['video_id']
        frame_number = row['frame_max_constricao']
        
        # Get the video path
        video_path = get_video_path_from_id(video_id, video_dir)
        
        # Get the frame
        frame = get_video_frame(video_id, frame_number, video_dir)
        
        if frame is not None:
            # Save the frame as an image
            output_path = os.path.join(output_dir, f"{video_id}_max_constriction.png")
            save_frame_as_image(frame, output_path)