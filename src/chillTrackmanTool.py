import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# Path to data directory
data_directory = "../data"

# Combine all CSV files into a single DataFrame
csv_files = glob.glob(os.path.join(data_directory, "*.csv"))
data = pd.concat([pd.read_csv(file) for file in csv_files], ignore_index=True)

# Get unique list of pitchers
pitchers = data['Pitcher'].unique()

# Function to plot Fastballs with given PlateLocHeight range (Low/High Pitches)
def plot_fastballs_low_high(pitcher_data, pitch_location_range, title_suffix, output_folder):
    filtered_data = pitcher_data[
        (pitcher_data['TaggedPitchType'] == 'Fastball') &
        (pitcher_data['PlateLocHeight'] >= pitch_location_range[0]) &
        (pitcher_data['PlateLocHeight'] <= pitch_location_range[1])
    ]
    averages = filtered_data[['VertApprAngle', 'InducedVertBreak', 'HorzBreak', 'SpinRate']].mean()

    fig, axes = plt.subplots(2, 3, figsize=(20, 12))

    bars = [
        ('VertApprAngle', averages['VertApprAngle'], 'skyblue', axes[0, 0]),
        ('InducedVertBreak', averages['InducedVertBreak'], 'lightgreen', axes[0, 1]),
        ('HorzBreak', averages['HorzBreak'], 'salmon', axes[0, 2]),
        ('SpinRate', averages['SpinRate'], 'gold', axes[1, 0]),
    ]
    for title, value, color, ax in bars:
        ax.bar([title], [value], color=color)
        ax.set_title(title)
        ax.text(0, value / 2, f"{value:.2f}", ha='center', va='center', color='black')
        ax.set_xticks([])  # Remove x-axis label

    filtered_righty = filtered_data[filtered_data['PlateLocSide'] <= 0]
    axes[1, 1].bar(['HorzApprAngle'], [filtered_righty['HorzApprAngle'].mean()], color='lightblue')
    axes[1, 1].set_title('HorzApprAngle (Inside to Righty)')
    axes[1, 1].text(
        0, filtered_righty['HorzApprAngle'].mean() / 2,
        f"{filtered_righty['HorzApprAngle'].mean():.2f}",
        ha='center', va='center', color='black'
    )
    axes[1, 1].set_xticks([])  # Remove x-axis label

    filtered_lefty = filtered_data[filtered_data['PlateLocSide'] > 0]
    axes[1, 2].bar(['HorzApprAngle'], [filtered_lefty['HorzApprAngle'].mean()], color='lightgreen')
    axes[1, 2].set_title('HorzApprAngle (Inside to Lefty)')
    axes[1, 2].text(
        0, filtered_lefty['HorzApprAngle'].mean() / 2,
        f"{filtered_lefty['HorzApprAngle'].mean():.2f}",
        ha='center', va='center', color='black'
    )
    axes[1, 2].set_xticks([])  # Remove x-axis label

    plt.suptitle(f'{pitcher_data["Pitcher"].iloc[0]} {title_suffix} Fastballs', fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    # Save figure to the folder
    output_file = os.path.join(output_folder, f'{title_suffix}_Fastballs.png')
    plt.savefig(output_file)
    plt.close()

# Function to plot averages for a specific range
def plot_avg(pitcher_data, pitch_location_range, title_suffix, plot_title, pitch_types, output_folder):
    filtered_data = pitcher_data[
        (pitcher_data['TaggedPitchType'].isin(pitch_types)) &
        (pitcher_data['PlateLocSide'] >= pitch_location_range[0]) &
        (pitcher_data['PlateLocSide'] <= pitch_location_range[1])
    ]

    # Determine metrics to display
    if set(pitch_types) == {'Curveball', 'Slider'}:
        metrics = ['InducedVertBreak', 'HorzBreak']
        colors = ['lightgreen', 'salmon']
    else:
        metrics = ['VertApprAngle', 'InducedVertBreak', 'HorzBreak', 'SpinRate']
        colors = ['skyblue', 'lightgreen', 'salmon', 'gold']

    averages = filtered_data[metrics].mean()

    rows = (len(metrics) + 1) // 2
    fig, axes = plt.subplots(rows, 2, figsize=(16, 6 * rows))

    for i, (metric, color) in enumerate(zip(metrics, colors)):
        row, col = divmod(i, 2)
        ax = axes[row, col] if rows > 1 else axes[col]
        value = averages[metric]
        ax.bar([metric], [value], color=color)
        ax.set_title(metric)
        ax.text(0, value / 2, f"{value:.2f}", ha='center', va='center', color='black')
        ax.set_xticks([])  # Remove x-axis label

    plt.suptitle(f'{pitcher_data["Pitcher"].iloc[0]} {title_suffix} {plot_title}', fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.95])

    # Save figure to the folder
    output_file = os.path.join(output_folder, f'{title_suffix}_{plot_title}.png')
    plt.savefig(output_file)
    plt.close()

# Iterate through all pitchers and create the plots
for pitcher in pitchers:
    pitcher_data = data[data['Pitcher'] == pitcher]
    
    # Create a directory for each pitcher
    pitcher_folder = os.path.join("output", pitcher)
    os.makedirs(pitcher_folder, exist_ok=True)
    
    # Print which pitcher is being processed
    print(f"Processing and saving plots for pitcher: {pitcher}")
    
    # Generate the plots for this pitcher
    plot_fastballs_low_high(pitcher_data, [1.0, 3.5], 'Low', pitcher_folder)  # Low Fastballs
    plot_fastballs_low_high(pitcher_data, [3.5, 6.5], 'High', pitcher_folder)  # High Fastballs
    plot_avg(pitcher_data, [-1.2, 0], '', 'Fastballs Inside to Righty', ['Fastball'], pitcher_folder)  # Fastballs Inside to Righty
    plot_avg(pitcher_data, [0, 1.2], '', 'Fastballs Inside to Lefty', ['Fastball'], pitcher_folder)  # Fastballs Inside to Lefty
    plot_avg(pitcher_data, [-1.2, 0], 'Inside to Righty', 'Curveballs and Sliders', ['Curveball', 'Slider'], pitcher_folder)  # Curveballs Inside to Righty
    plot_avg(pitcher_data, [0, 1.2], 'Inside to Lefty', 'Curveballs and Sliders', ['Curveball', 'Slider'], pitcher_folder)  # Curveballs Inside to Lefty

print("Figures saved successfully.")

