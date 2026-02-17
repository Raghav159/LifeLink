import numpy as np
import pandas as pd


# Sigmoid function converts any real number into probability (0–1)
# Used to simulate logistic regression style probability
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def generate_dataset(n_samples=5000, random_state=42):
    """
    Generate synthetic donor behavior dataset.

    n_samples: number of simulated donor-request interactions
    random_state: ensures reproducibility
    """

    # Set seed so results are reproducible
    np.random.seed(random_state)

    # -------------------------------
    # Generate input features
    # -------------------------------

    # Distance between donor and hospital (km)
    # Donors far away less likely to respond
    distance = np.random.uniform(0, 25, n_samples)

    # Days since last donation
    # Higher = more eligible + more likely to respond
    days_since_donation = np.random.uniform(90, 600, n_samples)

    # Urgency level (1=LOW, 2=MEDIUM, 3=HIGH)
    # Higher urgency increases response probability
    urgency = np.random.choice([1, 2, 3], n_samples)

    # Age of donor
    # Slightly younger donors may respond more
    age = np.random.uniform(18, 65, n_samples)

    # Whether donor is universal donor (O-)
    # Universal donors may be contacted more often
    is_universal = np.random.choice([0, 1], n_samples, p=[0.9, 0.1])

    # -------------------------------
    # Simulate behavioral logic
    # -------------------------------

    # Create a linear combination (logit)
    # These weights simulate real-world influence
    logit = (
        -0.12 * distance +              # further distance lowers response
        0.002 * days_since_donation +  # longer gap increases response
        0.8 * urgency +                # urgent request increases response
        0.4 * is_universal -           # universal donor bonus
        0.015 * age +                  # slight age penalty
        np.random.normal(0, 0.5, n_samples)  # noise for realism
    )

    # Convert logit into probability (0–1)
    probability = sigmoid(logit)

    # Simulate whether donor responded (0 or 1)
    # This makes dataset realistic (not deterministic)
    response = np.random.binomial(1, probability)

    # Create dataframe
    df = pd.DataFrame({
        "distance": distance,
        "days_since_donation": days_since_donation,
        "urgency": urgency,
        "age": age,
        "is_universal": is_universal,
        "response": response
    })

    return df
