import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Assuming Data is a pandas DataFrame
# pitcher_name = "Pitcher, Name"
# pitcher_data = Data[Data['Pitcher'] == pitcher_name]

# Replace this with your actual DataFrame
Data = pd.read_excel('Ashland.Game.1.xlsx')  # Placeholder for your data

# Filter data for the specific pitcher
pitcherName = input("Pitcher (Last, First):")
pitcher_data = Data[Data['Pitcher'] == "Tabor, Jacob"]

# Create the Summary Table
summary_table = pitcher_data.groupby('AutoPitchType').agg(
    Count=('AutoPitchType', 'size'),
    Avg_Velocity=('RelSpeed', 'mean'),
    Velocity_Max=('RelSpeed', 'max'),
    Avg_Spin=('SpinRate', 'mean'),
    IVB=('InducedVertBreak', 'mean'),
    HB=('HorzBreak', 'mean')
).reset_index()

print(summary_table)

# Create the Release Point Plot
plt.figure(figsize=(10, 6))
sns.scatterplot(data=pitcher_data, x='RelSide', y='RelHeight', hue='AutoPitchType', s=100)
plt.title('Pitcher Release Points by Pitch Type')
plt.xlabel('Release Side (feet)')
plt.ylabel('Release Height (feet)')
plt.xlim(-4, 4)
plt.ylim(-0.5, 8)
plt.axhline(0, linestyle='dashed', color='black')
plt.axvline(0, linestyle='dashed', color='black')
plt.legend(title='Pitch Type', loc='upper left')
plt.grid()
plt.show()

# Create the Plate Location Plot
plt.figure(figsize=(10, 6))
sns.scatterplot(data=pitcher_data, x='PlateLocSide', y='PlateLocHeight', hue='AutoPitchType', s=100)
plt.title('Plate Location Points By Pitch Type')
plt.xlabel('Plate Location Side')
plt.ylabel('Plate Location Height')
plt.xlim(-2, 2)
plt.ylim(0, 5)
plt.axhline(0, linestyle='dashed', color='black')
plt.axvline(0, linestyle='dashed', color='black')
plt.gca().add_patch(plt.Rectangle((-0.71, 1.5), 1.42, 2, fill=False, color='red', linestyle='dashed'))
plt.grid()
plt.show()

# Create the Pitch Movement Plot
plt.figure(figsize=(10, 6))
sns.scatterplot(data=pitcher_data, x='HorzBreak', y='InducedVertBreak', hue='AutoPitchType', s=100)
plt.title('Pitch Movement Points by Pitch Type')
plt.xlabel('Horizontal Break')
plt.ylabel('Induced Vertical Break')
plt.xlim(-30, 30)
plt.ylim(-30, 30)
plt.axhline(0, linestyle='dashed', color='black')
plt.axvline(0, linestyle='dashed', color='black')
plt.grid()
plt.show()

# Create the Pitcher Whiff Chart
swing_and_miss_data = Data[(Data['PitchCall'] == 'StrikeSwinging') & (Data['Pitcher'] == pitcherName)]

plt.figure(figsize=(10, 6))
sns.scatterplot(data=swing_and_miss_data, x='PlateLocSide', y='PlateLocHeight', hue='AutoPitchType', s=100)
plt.title('Plate Location of Swings and Misses')
plt.xlabel('Plate Location Side')
plt.ylabel('Plate Location Height')
plt.xlim(-2, 2)
plt.ylim(0, 5)
plt.axhline(0, linestyle='dashed', color='black')
plt.axvline(0, linestyle='dashed', color='black')
plt.gca().add_patch(plt.Rectangle((-0.71, 1.5), 1.42, 2, fill=False, color='red', linestyle='dashed'))
plt.grid()
plt.show()

# Create a scatter plot with facets for each AutoPitchType
sns.scatterplot(data=Data, x='SpinAxis', y='HorzBreak', hue='AutoPitchType', style='AutoPitchType', s=100, alpha=0.7)
plt.title('Effect of SpinAxis on Horizontal Break by AutoPitchType')
plt.xlabel('Spin Axis (degrees)')
plt.ylabel('Horizontal Break (inches)')
plt.axhline(0, linestyle='--', color='black', alpha=0.7)  # Add a horizontal line at y=0
plt.grid()
plt.legend(title='AutoPitch Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# Create a second plot for InducedVertBreak
plt.figure(figsize=(12, 6))
sns.scatterplot(data=Data, x='SpinAxis', y='InducedVertBreak', hue='AutoPitchType', style='AutoPitchType', s=100, alpha=0.7)
plt.title('Effect of SpinAxis on Induced Vertical Break by AutoPitchType')
plt.xlabel('Spin Axis (degrees)')
plt.ylabel('Induced Vertical Break (inches)')
plt.axhline(0, linestyle='--', color='black', alpha=0.7)  # Add a horizontal line at y=0
plt.grid()
plt.legend(title='AutoPitch Type', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
