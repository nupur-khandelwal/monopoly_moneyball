
import random
import pandas as pd

from board_simulator import simulate_monopoly
from analysis import analyze_properties

from analysis import analyze_properties, analyze_color_groups

from visualizations import (
    plot_landing_probabilities,
    plot_property_efficiency
)

random.seed(422)

# Run simulation
results = simulate_monopoly(100000)

# Analyze properties
df = analyze_properties(results["landing_counts"])

# Display results
pd.set_option("display.float_format", "{:.4f}".format)

print("\nMONOPOLY MONEYBALL - PROPERTY RANKINGS")
print(df.to_string(index=False))

# Export results
df.to_csv("property_analysis.csv", index=False)

print("\nSIMULATION STATISTICS")
print("Total turns:", results["num_turns"])
print("Total rolls:", results["total_rolls"])
print("Jail visits:", results["jail_visits"])
print("Recorded landings:", sum(results["landing_counts"]))

plot_landing_probabilities(results["landing_counts"])
plot_property_efficiency(df)

group_summary = analyze_color_groups(df)

print("\nCOLOR GROUP RANKINGS")
print(group_summary.to_string())