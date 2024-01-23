import data_loading
import data_processing
import visualization
import statistical_analysis
from constants import DATA_DIRECTORY
import pandas as pd
from tqdm import tqdm

def main():
    # Load and preprocess EEG data
    EEG_data = data_loading.load_and_preprocess_data(directory=DATA_DIRECTORY)

    # Define stimuli for analysis
    stimuli_list = ['S1 obj', 'S2 match']

    # Process, visualize, and analyze data for each stimulus
    for stimulus in tqdm(stimuli_list, desc="Processing stimuli"):
        try:
            # Sampling data for the current stimulus
            sampled_data = data_processing.sample_data(stimulus, EEG_data)

            # Channels and sensor positions for visualization
            channels = EEG_data[['sensor position', 'channel']].drop_duplicates().reset_index(drop=True).drop(['channel'], axis=1).reset_index(drop=False).rename(columns={'index':'channel'})['channel'].tolist()
            sensor_positions = EEG_data[['sensor position', 'channel']].drop_duplicates().reset_index(drop=True).drop(['channel'], axis=1).reset_index(drop=False).rename(columns={'index':'channel'})['sensor position'].tolist()

            # Visualization for each group
            for group in ['a', 'c']:
                visualization.plot_3dSurface_and_heatmap(stimulus, group, sampled_data, channels, sensor_positions)
            
            # Correlated pairs analysis
            corr_pairs_df = statistical_analysis.get_correlated_pairs(stimulus, 0.9, 'a', EEG_data,  channels)

            statistical_analysis.compare_corr_pairs(stimulus, corr_pairs_df)

            # Sensor correlation analysis
            statistical_analysis.plot_sensors_correlation(sampled_data, 0.97)

        except ValueError as e:
            print(f"Skipping {stimulus} due to error: {e}")


    # Mann Whitney U-test
    perform_mann_whitney_u_test(EEG_data)

def perform_mann_whitney_u_test(EEG_data):
    stat_test_results = pd.DataFrame({'stimulus': [], 'sensor': [], 'p_value': []})
    for sensor in tqdm(EEG_data['sensor position'].unique(), desc="Calculating U-tests"):
        for stimulus in EEG_data['matching condition'].unique():
            p_value = statistical_analysis.get_p_value(stimulus, sensor, EEG_data)
            new_row = pd.DataFrame({'stimulus': [stimulus], 'sensor': [sensor], 'p_value': [p_value]})
            stat_test_results = pd.concat([stat_test_results, new_row], ignore_index=True)

    stat_test_results['reject_null'] = stat_test_results['p_value'] <= 0.05
    visualization.visualize_significant_differences(stat_test_results)

if __name__ == "__main__":
    main()