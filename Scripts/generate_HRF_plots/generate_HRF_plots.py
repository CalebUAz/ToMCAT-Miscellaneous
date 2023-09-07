import argparse
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
from adjustText import adjust_text

def plot_save_fNIRS_HRF(df,output_path, filepath):
    # Extract animal and experiment names for title
    basename = os.path.basename(filepath)
    animal_name = basename.split('_')[-1].replace('.csv', '')
    experiment_name = filepath.split('/')[-2]
    
    # Identify the unique channel combinations
    channels = sorted(set([col.replace('_HbO', '').replace('_HbR', '') for col in df.columns if '_HbO' in col or '_HbR' in col]))
    
    # Determine the number of subplots
    n = len(channels) + 1  # Adding 1 for the average subplot
    
    fig, axs = plt.subplots(n, 1, figsize=(15, n*5))
    
    # Calculate the mean for HbO and HbR across all channels
    df['Mean_HbO'] = df[[f"{channel}_HbO" for channel in channels]].mean(axis=1)
    df['Mean_HbR'] = df[[f"{channel}_HbR" for channel in channels]].mean(axis=1)
    
    # Define a color mapping for each unique event_type
    event_colors = {
        'start_affective_task': '#1f78b4',  # A shade of blue
        'show_blank_screen': '#a6cee3',     # A lighter shade of blue
        'show_cross_screen': '#33a02c',     # A shade of green
        'show_image': '#e31a1c',            # A shade of red
        'show_rating_screen': '#ff7f00',    # A shade of orange
        'intermediate_selection': '#6a3d9a',# A shade of purple
        'final_submission': '#b15928'       # A shade of brown
    }
    
    for i, channel in enumerate(channels + ["Mean"]):
        if channel == "Mean":
            hbO_col, hbR_col = "Mean_HbO", "Mean_HbR"
        else:
            hbO_col, hbR_col = f"{channel}_HbO", f"{channel}_HbR"
        
        axs[i].plot(df.index * 0.1, df[hbO_col], label=hbO_col, color='red')
        axs[i].plot(df.index * 0.1, df[hbR_col], label=hbR_col, color='blue')
        
        # Placeholder entries for the legend
        axs[i].plot([], [], ' ', label='A: Arousal Score')
        axs[i].plot([], [], ' ', label='V: Valence Score')
        
        texts = []
        added_events = set()
    
        for idx, event in enumerate(df['event_type']):
            if pd.notna(event):
                if event not in added_events:
                    axs[i].axvline(x=idx * 0.1, linestyle='--', color=event_colors[event], label=f'Event: {event}')
                    added_events.add(event)
                else:
                    axs[i].axvline(x=idx * 0.1, linestyle='--', color=event_colors[event])
    
                if event == 'intermediate_selection':
                    arousal = df['arousal_score'].iloc[idx]
                    valence = df['valence_score'].iloc[idx]
    
                    # Display either arousal or valence based on which one is not NaN
                    if pd.notna(arousal):
                        score_text = f"A({arousal})"
                    else:
                        score_text = f"V({valence})"
                    
                    y_value = df[hbO_col].iloc[idx]
                    axs[i].scatter(idx * 0.1, y_value, color='black', s=20, zorder=3)
                    texts.append(axs[i].text(idx * 0.1, y_value + 0.1, score_text, color='black', verticalalignment='bottom', horizontalalignment='center'))
    
        adjust_text(texts, ax=axs[i], autoalign='xy', ha='right', va='bottom', only_move={'points':'y', 'text':'y'}, arrowprops=dict(arrowstyle='->', color='red', lw=0.5))
        
        handles, labels = axs[i].get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        axs[i].legend(by_label.values(), by_label.keys())
    
        if channel == "Mean":
            axs[i].set_title(f'Average of All Channels - {experiment_name} - {animal_name.capitalize()} Individual affective task')
        else:
            axs[i].set_title(f'{channel} - {experiment_name} - {animal_name.capitalize()} Individual affective task')
        
        axs[i].set_xlabel('Time (seconds)')
        axs[i].set_ylabel('Concentration (μmol/L)')
    
    plt.tight_layout()
    plt.savefig(output_path)
    
def parse_files(path, output_directory):
    ignore_df = pd.read_csv('./ignore_experimenter.csv')

    for root, dirs, files in os.walk(path):
            for folder in dirs:
                if folder.startswith('exp_'):
                    folder_path = os.path.join(root, folder)
                    
                    for file in os.listdir(folder_path):
                        if file.startswith('affective_individual_'):
                            file_path = os.path.join(folder_path, file)

                            # Check if file path contains an ignore combination
                            station = file.split('_')[-1].split('.')[0] # extract station name from the file name
                            ignore_rows = ignore_df[(ignore_df['group_session'] == folder) & (ignore_df['station'] == station)]
                            if not ignore_rows.empty:
                                print(f"Ignoring file {file_path} because experimenter was sitting there")
                                continue # Skip the rest and move to the next file

                            df = pd.read_csv(file_path)

                            # Extract the required sub-path
                            sub_path = os.path.join(*file_path.split(os.sep)[4:-1])  # The [4:-1] slice will vary based on your desired extraction
                            
                            # Construct the new directory path
                            new_dir = os.path.join(output_directory, sub_path)
                            os.makedirs(new_dir, exist_ok=True)  # Creates the directory if it doesn't exist
                            
                            # Formulate the filename from the original file's basename but with .png extension
                            filename = os.path.basename(file_path).replace('.csv', '.png')
                            
                            # Combine the new directory path with the filename
                            output_path = os.path.join(new_dir, filename)

                            plot_save_fNIRS_HRF(df,output_path, file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Post experiment script for xdf to csv file conversion"
    )
    parser.add_argument(
        "--p", required=True, help="Path to the directory with the fNIRS affective task data"
    )
    parser.add_argument(
        "--o", required=True, help="Path to the directory to save fNIRS HRF"
    )

    args = parser.parse_args()
    path = args.p
    output_directory = args.o

    sys.exit(parse_files(path, output_directory))