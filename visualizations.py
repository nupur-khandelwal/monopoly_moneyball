
import matplotlib.pyplot as plt


def plot_landing_probabilities(landing_counts):
    total_landings = sum(landing_counts)

    probabilities = [
        count / total_landings * 100
        for count in landing_counts
    ]

    spaces = list(range(40))

    plt.figure(figsize=(12, 5))
    plt.bar(spaces, probabilities)

    plt.axhline(
        y=2.5,
        color="red",
        linestyle="--",
        label="Uniform baseline (2.5%)"
    )

    plt.xlabel("Board Position")
    plt.ylabel("Landing Probability (%)")
    plt.title("Monopoly Landing Probabilities")
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_property_efficiency(df):
    plt.figure(figsize=(10, 8))

    plt.barh(
        df["Property"],
        df["Rent Efficiency"] * 100
    )

    plt.xlabel("Rent Efficiency (%)")
    plt.ylabel("Property")
    plt.title("Monopoly Property Investment Efficiency")

    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()
