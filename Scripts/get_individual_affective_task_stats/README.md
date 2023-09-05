# Affective Task Data Analysis

This script processes and visualizes data from individual affective task CSV files. It provides a hexbin plot, histograms, and bar graphs to analyze the arousal and valence scores from the data.

## Prerequisites

Ensure you have the following installed:

- Python 3.7 
- pandas
- matplotlib

## Structure

Your experiments should be structured as follows:
root_dir
└── exp_YYYY_MM_DD_HH
├── baseline_tasks
│ └── individual_*.csv


Each `individual_*.csv` file should be a semicolon-separated CSV file containing a columns called `image_path`, `arousal_score`, `valence_score` that this script will read and process entry with `final_submission`.

## Usage

1. Clone this repository or download the Python script to your local machine.

2. Navigate to the directory containing the script via terminal.

3. Run the script using the following command:

```bash
python3 script.py --input_path "/path/to/your/experiments"

```

Replace "/path/to/your/experiments" with the path to the directory containing your experiment directories.

The script will iterate over all the experiments and for each iMac, it will read the `individual_*.csv` file, plot the following:
1. Hexbin Plot: A hexbin plot of Arousal vs Valence Score with a jitter factor of 0.2.
2. Histograms: Histograms for both arousal and valence scores.
3. Bar Graphs: Bar graphs showing the mean arousal and valence scores for each image.

If an `individual_*.csv` file or an iMac folder is missing, the script will skip it and continue processing the next one.

