
import pandas as pd
from property_data import properties


def analyze_properties(landing_counts):
    total_landings = sum(landing_counts)
    landing_probabilities = []
    property_results = []

    # Calculate landing probabilities
    for count in landing_counts:
        probability = count / total_landings
        landing_probabilities.append(probability)

    # Calculate investment metrics
    for space in properties:
        property_info = properties[space]

        price = property_info["price"]
        rent = property_info["rent"]
        probability = landing_probabilities[space]

        expected_rent = probability * rent
        rent_efficiency = expected_rent / price

        property_results.append({
            "Property": property_info["name"],
            "Price": price,
            "Rent": rent,
            "Color Group": property_info["color_group"],
            "Landing Probability": probability,
            "Expected Rent": expected_rent,
            "Rent Efficiency": rent_efficiency
        })

    # Convert results into a DataFrame
    df = pd.DataFrame(property_results)

    # Rank properties by rent efficiency
    df = df.sort_values(
        by="Rent Efficiency",
        ascending=False
    )

    return df



def analyze_color_groups(df):
    group_summary = df.groupby("Color Group")[
        ["Price", "Expected Rent"]
    ].sum()

    group_summary["Group Efficiency (%)"] = (
        group_summary["Expected Rent"]
        / group_summary["Price"]
        * 100
    )

    group_summary = group_summary.sort_values(
        by="Group Efficiency (%)",
        ascending=False
    )

    return group_summary


def calculate_group_investment(properties, color_group, houses, landing_counts):
    if type(houses) is not int or not 0 <= houses <= 4:
        raise ValueError("Houses must be an integer between 0 and 4")

    purchase_cost = 0
    development_cost = 0
    total_rent = 0
    expected_rent = 0
    total_landings = sum(landing_counts)

    if total_landings == 0:
        raise ValueError("No recorded landings")

    for space, property_info in properties.items():

        if property_info["color_group"] == color_group:
            purchase_cost += property_info["price"]
            development_cost += houses * property_info["house_cost"]

            rent = property_info["rent_schedule"][houses]

            # Double base rent for an undeveloped monopoly
            if houses == 0:
                rent *= 2

            total_rent += rent

            landing_probability = landing_counts[space] / total_landings
            expected_rent += landing_probability * rent

    total_investment = purchase_cost + development_cost

    if total_investment == 0:
        raise ValueError("Invalid color group")

    investment_efficiency = expected_rent / total_investment

    return {
        "purchase_cost": purchase_cost,
        "development_cost": development_cost,
        "total_investment": total_investment,
        "total_rent": total_rent,
        "expected_rent": expected_rent,
        "investment_efficiency": investment_efficiency
    }

def compare_development_levels(properties, color_group, landing_counts):
    results = []
    for houses in range(5):
        investment = calculate_group_investment(properties, color_group, houses, landing_counts)
        results.append({
            "Houses": houses, 
            "Total Investment": investment["total_investment"],
            "Expected Rent": investment["expected_rent"],
            "Investment Efficiency": investment["investment_efficiency"]

        })

    df = pd.DataFrame(results)
    df = df.sort_values(
        by="Investment Efficiency",
        ascending=False
    )

    return df

def calculate_marginal_efficiency(df):
    #sort by number of houses
    df = df.sort_values(by= "Houses", ascending = True).copy()

    #calc the additional money invested
    df["Additional Investment"] = df["Total Investment"].diff()

    #calc additional expected rent
    df["Additional Expected Rent"] = df["Expected Rent"].diff()

    #calc marginal efficiency
    df["Marginal Efficiency"] = (df["Additional Expected Rent"] / df["Additional Investment"])

    return df



def compare_color_group_strategies(properties, landing_counts):
    results = []

    # Find all unique color groups
    color_groups = set()

    for property_info in properties.values():
        color_groups.add(property_info["color_group"])

    # Analyze each group
    for color_group in color_groups:
        df = compare_development_levels(
            properties,
            color_group,
            landing_counts
        )

        df = calculate_marginal_efficiency(df)

        # Find the development level with the highest efficiency
        best_row = df.loc[df["Investment Efficiency"].idxmax()]

        # Save the best strategy for this color group
        results.append({
            "Color Group": color_group,
            "Optimal Houses": int(best_row["Houses"]),
            "Total Investment": best_row["Total Investment"],
            "Expected Rent": best_row["Expected Rent"],
            "Investment Efficiency": best_row["Investment Efficiency"]
        })

    # Create a DataFrame of all groups
    comparison = pd.DataFrame(results)

    # Rank groups by investment efficiency
    comparison = comparison.sort_values(
        by="Investment Efficiency",
        ascending=False
    )

    return comparison

def generate_all_strategies(properties, landing_counts):
    results = []
    color_groups = set()

    for property_info in properties.values():
        color_groups.add(property_info["color_group"])

    for color_group in sorted(color_groups):
        df = compare_development_levels(properties, color_group, landing_counts)
        df["Color Group"] = color_group
        results.append(df)
        
    return pd.concat(results, ignore_index=True)


def optimize_budget(all_strategies, budget):
    if budget < 0:
        raise ValueError("Budget cannot be negative.")
    
    affordable = all_strategies[all_strategies["Total Investment"] <= budget]

    if affordable.empty:
        return affordable

    affordable = affordable.sort_values(
            by="Expected Rent",
            ascending=False
        )

    return affordable
    
