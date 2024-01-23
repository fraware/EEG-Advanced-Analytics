import pandas as pd
import os
import random
from constants import DATA_DIRECTORY, RANDOM_SEED, SENSOR_POSITION_MAPPINGS, EXCLUDED_SENSOR_POSITIONS

def load_and_preprocess_data(directory=DATA_DIRECTORY):
    """
    Loads and preprocesses EEG data from the specified directory.
    
    Parameters:
    directory (str): The path to the directory containing EEG data files.

    Returns:
    pd.DataFrame: Preprocessed EEG data.
    """
    random.seed(RANDOM_SEED)
    filenames_list = os.listdir(directory)
    data_frames = []

    for file_name in filenames_list:
        temp_df = pd.read_csv(os.path.join(directory, file_name))
        data_frames.append(temp_df)

    EEG_data = pd.concat(data_frames, ignore_index=True)
    EEG_data.drop(['Unnamed: 0'], axis=1, inplace=True)

    # Additional preprocessing steps
    for original, updated in SENSOR_POSITION_MAPPINGS.items():
        EEG_data.loc[EEG_data['sensor position'] == original, 'sensor position'] = updated
    EEG_data = EEG_data[~EEG_data['sensor position'].isin(EXCLUDED_SENSOR_POSITIONS)]

    return EEG_data