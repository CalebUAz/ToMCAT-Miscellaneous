import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import argparse
from adjustText import adjust_text

def plot_save_fNIRS_HRF(df, output_path, title=""):
    fig, ax = plt.subplots(figsize=(15, 5))

    hbO_col, hbR_col = "Mean_HbO", "Mean_HbR"

    ax.plot(df.index * 0.1, df[hbO_col], label=hbO_col, color='red')
    ax.plot(df.index * 0.1, df[hbR_col], label=hbR_col, color='blue')
    
    # Event-related code
    event_colors = {
        'start_affective_task': '#1f78b4',
        'show_blank_screen': '#a6cee3',
        'show_cross_screen': '#33a02c',
        'show_image': '#e31a1c',
        'show_rating_screen': '#ff7f00',
        'intermediate_selection': '#6a3d9a',
        'final_submission': '#b15928'
    }

    texts = []
    added_events = set()

    for idx, event in enumerate(df['event_type']):
        if pd.notna(event):
            if event not in added_events:
                ax.axvline(x=idx * 0.1, linestyle='--', color=event_colors[event], label=f'Event: {event}')
                added_events.add(event)
            else:
                ax.axvline(x=idx * 0.1, linestyle='--', color=event_colors[event])

            if event == 'intermediate_selection':
                arousal = df['arousal_score'].iloc[idx]
                valence = df['valence_score'].iloc[idx]

                if pd.notna(arousal):
                    score_text = f"A({arousal})"
                else:
                    score_text = f"V({valence})"
                
                y_value = df[hbO_col].iloc[idx]
                ax.scatter(idx * 0.1, y_value, color='black', s=20, zorder=3)
                texts.append(ax.text(idx * 0.1, y_value + 0.1, score_text, color='black', verticalalignment='bottom', horizontalalignment='center'))

    adjust_text(texts, ax=ax, autoalign='xy', ha='right', va='bottom', only_move={'points':'y', 'text':'y'}, arrowprops=dict(arrowstyle='->', color='red', lw=0.5))
    
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys())

    ax.set_title(title)
    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('Concentration (μmol/L)')

    plt.tight_layout()
    plt.savefig(output_path)
    print("Saving fNIRS HRF plot to {}".format(output_path))


def parse_files(path, output_directory):
    all_data = []

    print("-------------------------------------------------------------------------------------------------")
    print("Reading fNIRS affective task data from: {}".format(path))
    print("-------------------------------------------------------------------------------------------------")
    ignore_df = pd.read_csv('./ignore_experimenter.csv')

    for root, dirs, files in os.walk(path):
        for folder in dirs:
            if folder.startswith('exp_'):
                folder_path = os.path.join(root, folder)

                for file in os.listdir(folder_path):
                    if file.startswith('affective_individual_'):
                        file_path = os.path.join(folder_path, file)
                        station = file.split('_')[-1].split('.')[0]
                        ignore_rows = ignore_df[(ignore_df['group_session'] == folder) & (ignore_df['station'] == station)]
                        if not ignore_rows.empty:
                            print(f"Ignoring file {file_path} because experimenter was sitting there")
                            continue

                        df = pd.read_csv(file_path)
                        df.drop(columns='station', inplace=True)

                        if df.shape[1] == 45:
                            # Only keep the first 60 samples
                            df = df.iloc[:60]

                            # Accumulate the data for later averaging
                            all_data.append(df)

    # Calculate the average across all experiments
    avg_df = pd.concat(all_data).groupby(level=0).mean()

    # Now, call your plotting function with this average data
    avg_output_path = os.path.join(output_directory, "average_plot.png")
    plot_save_fNIRS_HRF(avg_df, avg_output_path, "Average Across Experiments")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Post experiment script for xdf to csv file conversion")
    parser.add_argument("--p", required=True, help="Path to the directory with the fNIRS affective task data")
    parser.add_argument("--o", required=True, help="Path to the directory to save fNIRS HRF")

    args = parser.parse_args()
    path = args.p
    output_directory = args.o

    sys.exit(parse_files(path, output_directory))
