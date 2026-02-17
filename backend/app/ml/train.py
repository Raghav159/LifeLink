import os
import json
import joblib
from datetime import datetime

import numpy as np

# Sklearn
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    roc_auc_score,
    confusion_matrix
)
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

from app.ml.data_generation import generate_dataset


def evaluate_model(model, X_test, y_test):
    """
    Evaluate model and return all important metrics.
    """

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    return {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_prob),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist()
    }


def train_model():
    """
    Full automated model comparison pipeline.
    """

    print("Generating dataset...")
    df = generate_dataset(n_samples=5000)

    X = df.drop("response", axis=1)
    y = df["response"]

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print("Training multiple models...")

    models = {
        "LogisticRegression": LogisticRegression(max_iter=1000),
        "RandomForest": RandomForestClassifier(n_estimators=200),
        "GradientBoosting": GradientBoostingClassifier()
    }

    results = {}
    best_model_name = None
    best_model = None
    best_score = -np.inf

    for name, model in models.items():
        print(f"Training {name}...")
        model.fit(X_train, y_train)

        metrics = evaluate_model(model, X_test, y_test)
        results[name] = metrics

        # Use ROC-AUC as selection metric
        if metrics["roc_auc"] > best_score:
            best_score = metrics["roc_auc"]
            best_model_name = name
            best_model = model

    print(f"Best model selected: {best_model_name}")
    print(f"Best ROC-AUC: {best_score}")

    # Create folders
    os.makedirs("app/ml/models", exist_ok=True)
    os.makedirs("app/ml/metrics", exist_ok=True)

    # Save best model
    model_path = "app/ml/models/model_v1.pkl"
    joblib.dump(best_model, model_path)

    # Save metrics
    metadata = {
        "best_model": best_model_name,
        "best_roc_auc": best_score,
        "all_model_metrics": results,
        "timestamp": datetime.utcnow().isoformat()
    }

    with open("app/ml/metrics/model_v1_metrics.json", "w") as f:
        json.dump(metadata, f, indent=4)

    print("Training complete.")
    print(json.dumps(metadata, indent=4))


if __name__ == "__main__":
    train_model()
