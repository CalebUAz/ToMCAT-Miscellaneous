# EEG Data Processing

This Python script is used to process EEG data from a collection of experiments. Each experiment consists of multiple stations (lion, tiger, leopard), and each station has an EEG data file.

## Prerequisites

Ensure you have the following installed:

- Python 3.7 or later
- pandas
- neurokit2

## Structure

Your experiments should be structured as follows:
root_dir
└── exp_YYYY_MM_DD_HH
├── lion
│ └── EEG.csv
├── tiger
│ └── EEG.csv
└── leopard
└── EEG.csv

Each `EEG.csv` file should be a semicolon-separated CSV file containing a column called `AUX_EKG` that this script will read and process.

## Usage

1. Clone this repository or download the Python script to your local machine.

2. Navigate to the directory containing the script via terminal.

3. Run the script using the following command:

```bash
python script.py --input_path "/path/to/your/experiments" --output_path "/path/to/save/EKG_quality_results.csv"

```

Replace "/path/to/your/experiments" with the path to the directory containing your experiment directories. Like wise replace "/path/to/save/_" with path where you want the output to be. 

The script will iterate over all the experiments and for each animal, it will read the EEG.csv file, compute the quality of the EEG data using neurokit2, and save the results in a CSV file named EKG_quality_results.csv in the same directory as your experiment directories.

If an EEG file or an animal folder is missing, the script will skip it and continue processing the next one.

## Output

The output file, EKG_quality_results.csv, will contain one row for each experiment, with columns for the experiment name and the calculated quality for each animal. If the quality could not be calculated (due to missing data, for example), the corresponding cell will contain None.
