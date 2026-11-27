def prepare_strategies(all_strategies, properties):
    grouped_strategies = {}

    color_groups = all_strategies["Color Group"].unique()
    for color_group in color_groups:

        strategies = [
            {
                "cost": 0,
                "rent": 0,
                "houses": None,
                "houses_required": 0,
                "hotels_required": 0
            }
        ]
        num_properties = 0

        for property_info in properties.values():
            if property_info["color_group"] == color_group:
                num_properties += 1

        group_df = all_strategies[all_strategies["Color Group"] == color_group]

        for index, row in group_df.iterrows():
            cost = int(row["Total Investment"])
            rent = float( row["Expected Rent"])
            houses = int(row["Houses"])

            if houses == 5:
                houses_required = 0
                hotels_required = num_properties
            else:
                houses_required = houses * num_properties
                hotels_required = 0

            strategies.append({
                "cost": cost,
                "rent": rent,
                "houses": houses,
                "houses_required": houses_required,
                "hotels_required": hotels_required
            })
        grouped_strategies[color_group] = strategies

    return grouped_strategies

def optimize_portfolio(grouped_strategies, budget, max_houses=32, max_hotels=12):
    if budget < 0:
        raise ValueError("Budget cannot be negative")

    if max_houses < 0 or max_hotels < 0:
        raise ValueError("Building limits cannot be negative")

    dp = {
        (0, 0, 0): {
            "rent": 0.0,
            "portfolio": []
        }
    }

    for color_group, strategies in grouped_strategies.items():

        new_dp = {}

        for (existing_cost, existing_houses, existing_hotels), state in dp.items():
            existing_rent = state["rent"]
            existing_portfolio = state["portfolio"]

            for strategy in strategies:

                new_cost = existing_cost + strategy["cost"]
                new_rent = existing_rent + strategy["rent"]
                new_houses = existing_houses + strategy["houses_required"]
                new_hotels = existing_hotels + strategy["hotels_required"]

                new_key = (new_cost, new_houses, new_hotels)

                if (
                    new_cost <= budget
                    and new_houses <= max_houses
                    and new_hotels <= max_hotels
                ):
                    if new_key not in new_dp or new_rent > new_dp[new_key]["rent"]:

                        new_portfolio = existing_portfolio.copy()

                        if strategy["houses"] is not None:
                            new_portfolio.append({
                                "color_group": color_group,
                                "houses": strategy["houses"],
                                "cost": strategy["cost"],
                                "rent": strategy["rent"],
                                "houses_required": strategy["houses_required"],
                                "hotels_required": strategy["hotels_required"]
                            })

                        new_dp[new_key] = {
                            "rent": new_rent,
                            "portfolio": new_portfolio
                        }

        dp = new_dp

    return dp