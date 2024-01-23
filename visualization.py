import pandas as pd
import plotly.graph_objs as go
from plotly.offline import iplot

def plot_3dSurface_and_heatmap(stimulus, group, df, channels, sensor_positions):
    # Mapping group identifiers to names
    group_names = {'c': 'Control', 'a': 'Alcoholic'}
    group_name = group_names.get(group, 'Unknown')

    # Creating pivot table
    pivot_df = pd.pivot_table(df[['channel', 'sample num', 'sensor value']],
                              index='channel', columns='sample num', values='sensor value')
    
    # Check if pivot table is created correctly
    if pivot_df.isnull().any().any():
        raise ValueError("Missing values in the data. Pivot table creation failed.")

    # Data for 3D surface plot
    data = [go.Surface(z=pivot_df.values, colorscale='Bluered')]

    # Layout configuration
    layout = go.Layout(
        title=f'3D Surface and Heatmap of Sensor Values: {stimulus} Stimulus - {group_name} Group',
        width=800,
        height=900,
        margin=dict(t=0, b=0, l=0, r=0),
        scene=dict(
            xaxis=dict(title='Time (sample num)', gridcolor='rgb(255, 255, 255)',
                       showbackground=True, backgroundcolor='rgb(230, 230,230)'),
            yaxis=dict(title='Channel', tickvals=list(range(len(channels))),
                       ticktext=sensor_positions, gridcolor='rgb(255, 255, 255)',
                       showbackground=True, backgroundcolor='rgb(230, 230, 230)'),
            zaxis=dict(title='Sensor Value', gridcolor='rgb(255, 255, 255)',
                       showbackground=True, backgroundcolor='rgb(230, 230,230)'),
            aspectratio=dict(x=1, y=1, z=0.7),
            aspectmode='manual'
        ),
        updatemenus=[dict(
            buttons=[
                dict(args=['type', 'surface'], label='3D Surface', method='restyle'),
                dict(args=['type', 'heatmap'], label='Heatmap', method='restyle')
            ],
            direction='left', pad={'r': 10, 't': 10}, showactive=True,
            type='buttons', x=0.1, xanchor='left', y=1.1, yanchor='top'
        )],
        annotations=[dict(text='Trace type:', x=0, y=1.085, yref='paper', align='left', showarrow=False)]
    )

    fig = go.Figure(data=data, layout=layout)
    iplot(fig)

def visualize_significant_differences(stat_test_results):
    """
    Visualizes significant differences based on Mann-Whitney U-test results.

    Parameters:
    stat_test_results (pd.DataFrame): DataFrame containing stimulus, sensor, p_value, and reject_null.
    """
    data = []

    # Unique stimuli in the test results
    stimuli = stat_test_results['stimulus'].unique()

    for stimulus in stimuli:
        # Filter the DataFrame for each stimulus
        filtered_df = stat_test_results[stat_test_results['stimulus'] == stimulus]

        # Create a bar chart for each stimulus
        trace = go.Bar(
            x=filtered_df['sensor'],
            y=filtered_df['reject_null'],
            name=stimulus
        )
        data.append(trace)

    # Define the layout of the chart
    layout = go.Layout(
        title='Significant Differences per Sensor for each Stimulus',
        xaxis=dict(title='Sensor'),
        yaxis=dict(title='Significant Difference (True/False)'),
        barmode='group'
    )

    # Create the figure and plot it
    fig = go.Figure(data=data, layout=layout)
    iplot(fig)