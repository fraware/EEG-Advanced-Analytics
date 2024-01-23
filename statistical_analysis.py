import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.offline import iplot
from scipy.stats import mannwhitneyu

def get_correlated_pairs_sample(threshold, list_of_pairs, group, correlation_df):
    """Identifies channel pairs with high correlation."""
    corr_pairs_dict = {pair: 0 for pair in list_of_pairs}

    for i, column in enumerate(correlation_df.columns):
        # Iterate only till the second last column to avoid index out of bounds
        if i < len(correlation_df.columns) - 1:
            series = correlation_df.iloc[i+1:, i]  # Lower triangle values
            for j, value in enumerate(series):
                # Ensure the index is within the range
                if i + j + 1 < len(correlation_df.columns):
                    pair = f'{column}-{correlation_df.columns[i + j + 1]}'
                    if pair in corr_pairs_dict:
                        corr_pairs_dict[pair] += 1

    corr_count = pd.DataFrame.from_dict(corr_pairs_dict, orient='index', columns=['count'])
    corr_count = corr_count[corr_count['count'] > 0].reset_index().rename(columns={'index': 'channel_pair'})
    print(f'Channel pairs with correlation >= {threshold} ({group} group): {corr_count["channel_pair"].tolist()}')

def plot_sensors_correlation(df, threshold_value):
    """Plots correlation heatmaps for sensor positions."""
    def generate_heatmap(sub_df, title):
        # Create the pivot table inside this function after filtering
        pivot_data = sub_df.pivot_table(values='sensor value', index='sample num', columns='sensor position').corr()
        mask = np.triu(np.ones_like(pivot_data, dtype=bool))
        cmap = sns.diverging_palette(220, 10, as_cmap=True)
        sns.heatmap(pivot_data, mask=mask, cmap=cmap, vmin=-1, vmax=1, center=0,
                    square=True, linewidths=.5, cbar_kws={"shrink": .5}).set_title(title)

    # Filter the DataFrame for each group before passing to generate_heatmap
    alcoholic_df = df[df['subject identifier'] == 'a']
    control_df = df[df['subject identifier'] == 'c']

    plt.figure(figsize=(17, 10))
    plt.subplot(121)
    generate_heatmap(alcoholic_df, 'Alcoholic group')

    plt.subplot(122)
    generate_heatmap(control_df, 'Control group')

    plt.suptitle(f'Correlation between Sensor Positions for {df["matching condition"].unique()[0]} stimulus', fontsize=16)
    plt.show()

    pivot_data = df.pivot_table(values='sensor value', index='sample num', columns='sensor position')

    # Generate list_of_pairs
    list_of_pairs = []
    for i, col1 in enumerate(pivot_data.columns):
        for col2 in pivot_data.columns[i + 1:]:
            list_of_pairs.append(f"{col1}-{col2}")

    get_correlated_pairs_sample(threshold=threshold_value, correlation_df=pivot_data, group='Alcoholic', list_of_pairs=list_of_pairs)
    get_correlated_pairs_sample(threshold=threshold_value, correlation_df=pivot_data, group='Control', list_of_pairs=list_of_pairs)

def get_correlated_pairs(stimulus, threshold, group, EEG_data, channels):
    """Returns dataframe with high correlation channel pairs for given stimulus and group."""
    # Initialize an empty dictionary to store pair counts
    corr_pairs_dict = {}

    for trial_number in EEG_data['trial number'][(EEG_data['subject identifier'] == group) & 
                                                  (EEG_data['matching condition'] == stimulus)].unique():
        sub_df = EEG_data[(EEG_data['subject identifier'] == group) & 
                          (EEG_data['trial number'] == trial_number)]
        pivot_data = sub_df.pivot_table(values='sensor value', index='sample num', columns='sensor position').corr()

        for idx, column in enumerate(pivot_data.columns):
            for i in range(idx + 1, len(pivot_data.columns)):
                value = pivot_data.at[column, pivot_data.columns[i]]
                if value >= threshold:
                    pair = f'{column}-{pivot_data.columns[i]}'
                    # Dynamically add the pair to the dictionary if not present
                    corr_pairs_dict[pair] = corr_pairs_dict.get(pair, 0) + 1

    # Convert the dictionary to a DataFrame
    corr_count = pd.DataFrame(list(corr_pairs_dict.items()), columns=['channel_pair', 'count'])
    corr_count['group'] = group
    corr_count['stimulus'] = stimulus
    return corr_count

def compare_corr_pairs(stimulus, corr_pairs_df):
    # Check if 'group' column exists in corr_pairs_df
    if 'group' not in corr_pairs_df.columns:
        raise ValueError("The DataFrame does not contain the 'group' column.")

    # Assuming corr_pairs_df has the columns 'group', 'stimulus', 'channel_pair', 'count'
    top_pairs = corr_pairs_df.sort_values('count', ascending=False).head(20)

    # Filter the data for each group and create the bar chart
    def create_bar(data, name, color):
        return go.Bar(x=data['channel_pair'], y=data['count'],
                      text=data['count'], name=name, marker=dict(color=color))

    data_a = top_pairs[top_pairs['group'] == 'a']
    data_c = top_pairs[top_pairs['group'] == 'c']

    data = [create_bar(data_a, 'Alcoholic Group', 'rgb(20,140,45)'),
            create_bar(data_c, 'Control Group', 'rgb(200,100,45)')]

    layout = go.Layout(title=f'Correlated Pairs Ratio ({stimulus} stimulus)',
                       xaxis=dict(title='Channel Pairs'), yaxis=dict(title='Count'), barmode='group')
    fig = go.Figure(data=data, layout=layout)
    iplot(fig)

def get_p_value(stimulus, sensor, EEG_data):
    """Calculates Mann Whitney U-test p-value for Alcoholic vs Control."""
    x = EEG_data['sensor value'][(EEG_data['subject identifier'] == 'a') & 
                                 (EEG_data['matching condition'] == stimulus) & 
                                 (EEG_data['sensor position'] == sensor)]
    y = EEG_data['sensor value'][(EEG_data['subject identifier'] == 'c') & 
                                 (EEG_data['matching condition'] == stimulus) & 
                                 (EEG_data['sensor position'] == sensor)]
    return mannwhitneyu(x, y, alternative='two-sided')[1]
