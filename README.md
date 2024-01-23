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
