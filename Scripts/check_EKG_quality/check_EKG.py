import os
import pandas as pd
import neurokit2 as nk
import argparse

# Create the parser and add arguments
parser = argparse.ArgumentParser(description='Process EEG data.')
parser.add_argument('--input_path', type=str, help='The root path to your experiment folders')
parser.add_argument('--output_path', type=str, help='The path where the results should be written')
args = parser.parse_args()

# The absolute path to your experiment folders
root_dir = args.input_path

# Get the list of all experiment folders
exp_dirs = [os.path.join(root_dir, dir) for dir in os.listdir(root_dir) if dir.startswith('exp_')]

results = []

# Iterate through all experiment directories
for exp_dir in exp_dirs:
    exp_dir_name = os.path.basename(exp_dir)  # Get the name of the experiment directory
    result_row = {'exp_dir': exp_dir_name}
    # Go through each imac folder (lion, tiger, leopard)
    for imac in ['lion', 'tiger', 'leopard']:
        try:
            # Load the EEG.csv file
            eeg_file = os.path.join(exp_dir, imac, 'EEG.csv')
            # Specify the semicolon delimiter
            df = pd.read_csv(eeg_file, delimiter=';')
            # Get the AUX_EKG column
            EKG = df['AUX_EKG']
            EKG *= 1e-6  # Convert to microvolts

            # Pass it to neurokit2
            cleaned = nk.ecg_clean(EKG, sampling_rate=500, method="biosppy")
            rpeaks = nk.ecg_findpeaks(cleaned, method='pantompkins')
            quality = nk.ecg_quality(cleaned, sampling_rate=500, rpeaks=rpeaks, method='zhao2018')

            result_row[imac] = quality
        except (FileNotFoundError, pd.errors.EmptyDataError, KeyError):
            print(f"Error processing {imac} in {exp_dir_name}. EEG.csv file or AUX_EKG column may be missing.")
            result_row[imac] = None  # Assign None or an appropriate value for missing data

    results.append(result_row)

# Convert the results into a pandas DataFrame and write to a csv
df_results = pd.DataFrame(results)
df_results.to_csv(args.output_path, index=False)
