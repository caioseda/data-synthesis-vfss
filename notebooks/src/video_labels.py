import pandas as pd

def normalize_columns_names(columns):
    """
    Normalize the column names of a DataFrame by removing leading/trailing whitespace and converting to lowercase.
    """
    columns = (
        columns
        .str.replace(' ', '_')
        # .str.normalize('NFKD')
        .str.encode('ascii', errors='ignore')
        .str.decode('utf-8')
        .str.lower()
    )
    return columns

def read_video_labels_df(path):
    """
    Read the rotulos DataFrame from an Excel file and normalize its column names.
    """
    # df_frames_pas = pd.read_excel('../data/rotulos/Frames e PAS.xlsx')
    df = pd.read_excel(path)
    
    # Rename columns to remove leading/trailing whitespace
    df.columns = normalize_columns_names(df.columns)

    # Rename columns
    df = df.rename(columns={
        'frame_de_mxima_constrio_farngea': 'frame_max_constricao',
        'frame_de_repouso': 'frame_repouso',
        'pas_frame': 'pas_frame',
        'pas': 'pas_score',
        'video': 'video_id'
    })
    df = df.dropna(subset=['video_id'])

    df['video_id'] = df['video_id'].astype(int)
    df['frame_max_constricao'] = df['frame_max_constricao'].astype(int)
    # df['frame_repouso'] = df['frame_repouso'].astype(int)
    df['pas_frame'] = df['pas_frame'].astype(float)
    df['pas_score'] = df['pas_score'].astype(float)


    return df