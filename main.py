
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

# # Analyze properties
# df = analyze_properties(results["landing_counts"])

# # Display results
# pd.set_option("display.float_format", "{:.4f}".format)

# print("\nMONOPOLY MONEYBALL - PROPERTY RANKINGS")
# print(df.to_string(index=False))

# # Export results
# df.to_csv("property_analysis.csv", index=False)

# print("\nSIMULATION STATISTICS")
# print("Total turns:", results["num_turns"])
# print("Total rolls:", results["total_rolls"])
# print("Jail visits:", results["jail_visits"])
# print("Recorded landings:", sum(results["landing_counts"]))

# plot_landing_probabilities(results["landing_counts"])
# plot_property_efficiency(df)

# group_summary = analyze_color_groups(df)

# print("\nCOLOR GROUP RANKINGS")
# print(group_summary.to_string())

from property_data import properties
from analysis import calculate_group_investment, compare_development_levels, calculate_marginal_efficiency
from analysis import compare_color_group_strategies

# group_comparison = compare_color_group_strategies(
#     properties,
#     results["landing_counts"]
# )

# print("\nMONOPOLY COLOR GROUP STRATEGY RANKINGS")
# print(group_comparison.to_string(index=False))

from analysis import generate_all_strategies

all_strategies = generate_all_strategies(
    properties,
    results["landing_counts"]
)

# print("\nALL INVESTMENT STRATEGIES")
# print(all_strategies.to_string(index=False))
# print("Total strategies:", len(all_strategies))

from analysis import optimize_budget

budget = 1500

optimized = optimize_budget(all_strategies, budget)

# print(calculate_group_investment(
#     properties,
#     "Orange",
#     5,
#     results["landing_counts"]
# ))

from optimization import prepare_strategies

grouped = prepare_strategies(all_strategies)

from optimization import optimize_portfolio

budgets = [0, 100, 120, 500, 620, 1000, 1500, 
           2000, 3000, 5000, 10000, 100000]

for budget in budgets:
    dp = optimize_portfolio(grouped, budget)

    best_cost = max(dp, key=lambda cost: dp[cost]["rent"])
    best_state = dp[best_cost]

        # Verify that the portfolio is affordable
    assert best_cost <= budget

    # Verify that the portfolio cost matches the DP state
    assert sum(s["cost"] for s in best_state["portfolio"]) == best_cost

    # Verify that no color group appears twice
    groups = [s["color_group"] for s in best_state["portfolio"]]
    assert len(groups) == len(set(groups))

    # Verify that expected rent matches the DP state
    assert abs(
        sum(s["rent"] for s in best_state["portfolio"])
        - best_state["rent"]
    ) < 1e-9