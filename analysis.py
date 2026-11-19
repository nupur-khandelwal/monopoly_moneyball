
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
