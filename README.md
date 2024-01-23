# EEG Advanced Analysis for Cognitive State Identification

This repository hosts a Python-based project aimed at analyzing EEG (Electroencephalogram) data to identify different cognitive states, focusing on comparing control and alcoholic subjects. The project employs statistical and data visualization techniques to explore EEG datasets.

## Project Overview

This project is structured to handle EEG data through various processing and analysis stages. It's divided into several modules:

- `data_loading.py`: For loading and preprocessing the EEG dataset.
- `data_processing.py`: Manages data sampling and preparation for analysis.
- `visualization.py`: Contains functions for data visualization, including 3D surface plots and heatmaps.
- `statistical_analysis.py`: Handles statistical analysis, including correlation analysis and Mann-Whitney U-tests.
- `main.py`: The main script that orchestrates the execution of the project.

Developed using **Python 3.12**, the project is designed to be clear, modular, and extendable.

## Data Source

The EEG data used in this project is sourced from the [EEG Database at UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/121/eeg+database). This database originates from a comprehensive study aimed at examining EEG correlates of genetic predisposition to alcoholism.

### Dataset Characteristics
- **Type:** Multivariate, Time-Series
- **Subject Area:** Health and Medicine
- **Tasks:** Classification
- **Feature Types:** Categorical, Integer, Real
- **Number of Instances:** 122

### Dataset Information
The dataset includes measurements from 64 electrodes placed on subjects' scalps, sampled at 256 Hz (3.9-msec epoch) for 1 second. The study involved two groups of subjects: alcoholic and control. Each subject was exposed to different stimuli, either a single stimulus (S1) or two stimuli (S1 and S2), where S1 and S2 could be identical or different.

### Additional Notes
- **Electrode Placement:** Standard sites (Standard Electrode Position Nomenclature, American Electroencephalographic Association 1990).
- **Data Collection:** Detailed in Zhang et al. (1995).
- **Data Issues:** Some trials have "err" notices, and there are 17 trials with empty files in one of the datasets.

Example plots of control and alcoholic subjects' data under single stimulus conditions can be found on the [UCI Repository site](http://kdd.ics.uci.edu/databases/eeg/eeg.html).

This dataset provides a rich source for examining EEG-based differences between control and alcoholic subjects, forming the basis of our analysis in this project.

## Setup and Installation

To set up the project:

1. **Clone the Repository**

2. **Install Dependencies**
   All dependencies are listed in `requirements.txt`. Install them using:

```bash
  pip install -r requirements.txt
```

3. **Run the Project**
   Execute the main script to start the process:

```bash
python main.py
```

## Setup and Installation

The project analyzes EEG data, focusing on variations between control and alcoholic subjects. The data is processed to highlight differences in sensor values, correlation between different EEG channels, and statistical significance of these variations.

## Visualization and Analysis

The project outputs include:

1. 3D surface and heatmap visualizations of EEG sensor data.
2. Correlation analysis between different EEG sensors.
3. Statistical analysis results, including Mann-Whitney U-test outcomes.

## References

This project is inspired by various studies and papers on EEG data analysis and cognitive state identification:

1. Johnstone, S. J., et al. (2007). Functional brain mapping of psychopathology. Journal of Clinical Neurophysiology, 24(3), 275-290.
2. Davidson, R. J. (2004). Well-being and affective style: Neural substrates and biobehavioral correlates. Philosophical Transactions of the Royal Society of London. Series B, Biological Sciences, 359(1449), 1395-1411.
3. Knyazev, G. G. (2007). Motivation, emotion, and their inhibitory control mirrored in brain oscillations. Neuroscience and Biobehavioral Reviews, 31(3), 377-395.
