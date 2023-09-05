import os
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Create the parser and add arguments
parser = argparse.ArgumentParser(description='Get stats from individual affective task CSV files.')
parser.add_argument('--input_path', type=str, help='The root path to your experiment folders')

args = parser.parse_args()

# Define your specific path here (leave it as None if not specified)
specific_path = None

# If no specific path is provided, set the path to an 'output' folder in the same directory as the script
if specific_path is None:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, 'output')
else:
    output_path = specific_path

# Create the output directory if it doesn't exist
if not os.path.exists(output_path):
    os.makedirs(output_path)

# The absolute path to your experiment folders
root_dir = args.input_path

# Initialize an empty dataframe to store the final results
master_df = pd.DataFrame()

# Traverse the root directory
for dir_name in os.listdir(root_dir):
    if dir_name.startswith('exp_') and dir_name not in ['exp_2022_04_22_09','exp_2022_04_01_13']:
        #print(dir_name)
        
        affective_dir = os.path.join(root_dir, dir_name, 'baseline_tasks', 'affective')
        
        # Check if the affective directory exists
        if os.path.exists(affective_dir):
            for file_name in os.listdir(affective_dir):
                if file_name.startswith('individual_') and file_name.endswith('.csv'):
                    
                    file_path = os.path.join(affective_dir, file_name)
                    #print(file_path)
                    # Read the CSV file into a dataframe
                    df = pd.read_csv(file_path, sep=';')
                    
                    # Filter the dataframe
                    filtered_df = df[df['event_type'] == 'final_submission'][['image_path', 'arousal_score', 'valence_score']]
                    
                    # Append the filtered dataframe to the master dataframe
                    master_df = pd.concat([master_df, filtered_df], ignore_index=True)

# The master_df now contains the appended data from all the individual CSV files
#print(master_df)

jitter = 0.2
master_df['arousal_score_jittered'] = master_df['arousal_score'] + jitter * (np.random.rand(len(master_df)) - 0.5)
master_df['valence_score_jittered'] = master_df['valence_score'] + jitter * (np.random.rand(len(master_df)) - 0.5)

# Hexbin plot
plt.hexbin(master_df['arousal_score_jittered'], master_df['valence_score_jittered'], gridsize=20, cmap='Blues')
plt.colorbar(label='Count in bin')
plt.title('Hex bin plot of Arousal vs Valence Score with jitter factor of 0.2')
plt.xlabel('Arousal Score')
plt.ylabel('Valence Score')
plt.savefig(os.path.join(output_path, 'hexbin_plot.png'))
plt.show()

# Histogram for arousal_score
plt.figure(figsize=(10, 6))
plt.hist(master_df['arousal_score'], bins=5, edgecolor='black')
plt.title('Histogram of Arousal Score')
plt.xlabel('Arousal Score')
plt.ylabel('Frequency')
plt.savefig(os.path.join(output_path, 'histogram_arousal.png'))
plt.show()

# Histogram for valence_score
plt.figure(figsize=(10, 6))
plt.hist(master_df['valence_score'], bins=5, edgecolor='black')
plt.title('Histogram of Valence Score')
plt.xlabel('Valence Score')
plt.ylabel('Frequency')
plt.savefig(os.path.join(output_path, 'histogram_valence.png'))
plt.show()

# Bar graph for mean arousal_score of each image
mean_arousal = master_df.groupby('image_path')['arousal_score'].mean()
plt.figure(figsize=(10, 6))
mean_arousal.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Bar Graph of Mean Arousal Score per Image')
plt.xlabel('Image Path')
plt.ylabel('Mean Arousal Score')
plt.xticks(rotation=45)
plt.savefig(os.path.join(output_path, 'bar_graph_arousal.png'))
plt.show()

# Bar graph for mean valence_score of each image
mean_valence = master_df.groupby('image_path')['valence_score'].mean()
plt.figure(figsize=(10, 6))
mean_valence.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Bar Graph of Mean Valence Score per Image')
plt.xlabel('Image Path')
plt.ylabel('Mean Valence Score')
plt.xticks(rotation=45)
plt.savefig(os.path.join(output_path, 'bar_graph_valence.png'))
plt.show()