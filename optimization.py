def prepare_strategies(all_strategies):
    grouped_strategies = {}

    color_groups = all_strategies["Color Group"].unique()
    for color_group in color_groups:

        strategies = [
            {"cost": 0, "rent": 0, "houses": None}
        ]

        group_df = all_strategies[all_strategies["Color Group"] == color_group]

        for index, row in group_df.iterrows():
            cost = int(row["Total Investment"])
            rent = float( row["Expected Rent"])
            houses = int(row["Houses"])

            strategies.append({
            "cost": cost,
            "rent": rent,
            "houses": houses
            })
        grouped_strategies[color_group] = strategies

    return grouped_strategies


def optimize_portfolio(grouped_strategies, budget):
    if budget < 0:
        raise ValueError("Budget cannot be negative")

    dp = {
    0: {
        "rent": 0.0,
        "portfolio": []
    }
}

def optimize_portfolio(grouped_strategies, budget):
    if budget < 0:
        raise ValueError("Budget cannot be negative")

    dp = {
        0: {
            "rent": 0.0,
            "portfolio": []
        }
    }

    for color_group, strategies in grouped_strategies.items():

        new_dp = {}

        for existing_cost, state in dp.items():
            existing_rent = state["rent"]
            existing_portfolio = state["portfolio"]

            for strategy in strategies:

                new_cost = existing_cost + strategy["cost"]
                new_rent = existing_rent + strategy["rent"]

                if new_cost <= budget:
                    if new_cost not in new_dp or new_rent > new_dp[new_cost]["rent"]:

                        new_portfolio = existing_portfolio.copy()

                        if strategy["houses"] is not None:
                            new_portfolio.append({
                                "color_group": color_group,
                                "houses": strategy["houses"],
                                "cost": strategy["cost"],
                                "rent": strategy["rent"]
                            })

                        new_dp[new_cost] = {
                            "rent": new_rent,
                            "portfolio": new_portfolio
                        }

        dp = new_dp

    return dp