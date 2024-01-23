import pandas as pd
import random
from constants import RANDOM_SEED

def sample_data(stimulus, EEG_data, random_id=None):
    """
    Merges data frames for randomly selected subjects from control and alcoholic groups based on the stimulus.
    :param stimulus: The stimulus condition to filter the data.
    :param EEG_data: DataFrame containing EEG data.
    :param random_id: Optional random index for subject selection. If None, a random index is generated.
    :return: DataFrame combined from both selected subjects.
    """
    random.seed(RANDOM_SEED)

    if not isinstance(EEG_data, pd.DataFrame):
        raise ValueError("EEG_data must be a pandas DataFrame.")

    # Random ID generation within the valid range
    max_id = EEG_data['name'].nunique() - 1
    random_id = random.randint(0, max_id) if random_id is None else random_id

    # Ensuring random_id is within range
    if not (0 <= random_id <= max_id):
        raise ValueError(f"random_id must be between 0 and {max_id}")

    # Selecting IDs for alcoholic and control subjects
    subject_ids = EEG_data['name'][EEG_data['matching condition'] == stimulus].unique()
    if len(subject_ids) < 2:
        raise ValueError("Not enough subjects for the given stimulus condition.")

    alcoholic_id, control_id = subject_ids[:2]

    # Filtering data for minimum trial number for each group
    filter_alcoholic = (EEG_data['name'] == alcoholic_id) & (EEG_data['matching condition'] == stimulus)
    filter_control = (EEG_data['name'] == control_id) & (EEG_data['matching condition'] == stimulus)
    
    min_trial_alcoholic = EEG_data['trial number'][filter_alcoholic].min()
    min_trial_control = EEG_data['trial number'][filter_control].min()

    # Constructing the final DataFrame
    alcoholic_df = EEG_data[filter_alcoholic & (EEG_data['trial number'] == min_trial_alcoholic)]
    control_df = EEG_data[filter_control & (EEG_data['trial number'] == min_trial_control)]

    return pd.concat([alcoholic_df, control_df])
