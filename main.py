
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

grouped = prepare_strategies(all_strategies, properties)

from optimization import optimize_portfolio
scenarios = [
    (3000, 32, 12),
    (3000, 0, 12),
    (3000, 32, 0),
    (3000, 0, 0),
    (3000, 6, 3),
    (0, 32, 12),
    (10000, 32, 12),
    (100000, 32, 12)
]

for budget, max_houses, max_hotels in scenarios:

    dp = optimize_portfolio(
        grouped,
        budget,
        max_houses,
        max_hotels
    )

    best_key = max(dp, key=lambda key: dp[key]["rent"])
    best_state = dp[best_key]

    cost, houses_used, hotels_used = best_key

    print(f"\nBudget: ${budget}")
    print(f"House limit: {max_houses}")
    print(f"Hotel limit: {max_hotels}")

    print(f"Investment: ${cost}")
    print(f"Expected rent: ${best_state['rent']:.4f}")
    print(f"Houses used: {houses_used}")
    print(f"Hotels used: {hotels_used}")

    for strategy in best_state["portfolio"]:
        print(strategy)
        portfolio = best_state["portfolio"]

        # Verify resource constraints
        assert cost <= budget
        assert houses_used <= max_houses
        assert hotels_used <= max_hotels

        # Verify portfolio totals
        assert sum(s["cost"] for s in portfolio) == cost

        assert sum(
            s["houses_required"] for s in portfolio
        ) == houses_used

        assert sum(
            s["hotels_required"] for s in portfolio
        ) == hotels_used

        # Verify unique color groups
        groups = [s["color_group"] for s in portfolio]
        assert len(groups) == len(set(groups))

        # Verify expected rent
        assert abs(
            sum(s["rent"] for s in portfolio)
            - best_state["rent"]
        ) < 1e-9

print(f"\nAll {len(scenarios) * 8} checks passed!")