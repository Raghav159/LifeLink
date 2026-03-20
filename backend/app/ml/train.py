import os
import json
import logging
import joblib
from datetime import datetime
from typing import Tuple

import numpy as np

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    roc_auc_score,
    f1_score,
    confusion_matrix
)
from xgboost import XGBClassifier

from app.ml.data_generation import generate_synthetic_data

logger = logging.getLogger(__name__)


def train_model(model_path: str = "app/ml/models/model_v1.pkl") -> XGBClassifier:
    """
    Full ML training pipeline with XGBoost:
    1. Generate 10,000 synthetic donor-request pairs
    2. Stratified train/val/test split (80/10/10)
    3. Hyperparameter tuning via GridSearchCV (5-fold CV)
    4. Train final model on train+val combined
    5. Evaluate on test set
    6. Save model + metrics
    
    Target Metrics: Accuracy 90%+, Precision ≥ 90%, Recall ≥ 85%, F1 ≥ 0.87
    """
    
    logger.info("=" * 60)
    logger.info("🚀 Starting XGBoost Model Training Pipeline")
    logger.info("=" * 60)
    
    # 1. Generate synthetic data
    logger.info("📊 Generating 10,000 synthetic donor-request pairs...")
    X, y = generate_synthetic_data(n_samples=10000)
    logger.info(f"✅ Data generated: X.shape={X.shape}, y.shape={y.shape}")
    
    # 2. Stratified split (80/10/10)
    logger.info("🔀 Performing stratified train/val/test split (80/10/10)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.1, stratify=y, random_state=42
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=0.11, stratify=y_train, random_state=42
    )
    logger.info(f"Train: {X_train.shape}, Val: {X_val.shape}, Test: {X_test.shape}")
    
    # 3. Hyperparameter tuning with GridSearchCV
    logger.info("🔧 Hyperparameter tuning with GridSearchCV (5-fold CV)...")
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [5, 6, 7],
        'learning_rate': [0.05, 0.1],
    }
    
    xgb_base = XGBClassifier(
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=3,  # Handle class imbalance
        random_state=42,
        verbosity=0
    )
    
    grid_search = GridSearchCV(
        xgb_base, param_grid, cv=5, scoring='f1', n_jobs=-1, verbose=1
    )
    grid_search.fit(X_train, y_train)
    
    best_params = grid_search.best_params_
    logger.info(f"✅ Best parameters found: {best_params}")
    logger.info(f"   Best CV F1 Score: {grid_search.best_score_:.4f}")
    
    best_model = grid_search.best_estimator_
    
    # 4. Train on train + val combined
    logger.info("🎯 Retraining on combined train+val set...")
    X_combined = np.vstack([X_train, X_val])
    y_combined = np.hstack([y_train, y_val])
    best_model.fit(X_combined, y_combined)
    
    # 5. Evaluate on test set
    logger.info("📈 Evaluating on held-out test set...")
    y_pred = best_model.predict(X_test)
    y_pred_proba = best_model.predict_proba(X_test)[:, 1]
    
    metrics = {
        'accuracy': float(accuracy_score(y_test, y_pred)),
        'precision': float(precision_score(y_test, y_pred)),
        'recall': float(recall_score(y_test, y_pred)),
        'f1': float(f1_score(y_test, y_pred)),
        'roc_auc': float(roc_auc_score(y_test, y_pred_proba)),
        'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
    }
    
    logger.info("📊 Test Set Metrics:")
    logger.info(f"   Accuracy:  {metrics['accuracy']:.4f} (Target: 90%+)")
    logger.info(f"   Precision: {metrics['precision']:.4f} (Target: ≥90%)")
    logger.info(f"   Recall:    {metrics['recall']:.4f} (Target: ≥85%)")
    logger.info(f"   F1 Score:  {metrics['f1']:.4f} (Target: ≥0.87)")
    logger.info(f"   ROC-AUC:   {metrics['roc_auc']:.4f}")
    
    # 6. Save model + metrics
    logger.info("💾 Saving model and metrics...")
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(best_model, model_path)
    logger.info(f"✅ Model saved to {model_path}")
    
    metrics_path = model_path.replace('.pkl', '_metrics.json')
    metadata = {
        'timestamp': datetime.utcnow().isoformat(),
        'model_type': 'XGBClassifier',
        'best_params': best_params,
        'best_cv_f1': float(grid_search.best_score_),
        'metrics': metrics,
        'feature_count': 14,
        'features': [
            'distance_km', 'days_since_donation', 'age', 'is_universal_donor',
            'donation_frequency_6m', 'successful_previous_matches', 'has_adverse_reactions',
            'urgency_numeric', 'quantity_ml', 'patient_age', 'request_hour',
            'age_compatibility', 'distance_urgency_score', 'recency_urgency_score'
        ]
    }
    
    with open(metrics_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    logger.info(f"✅ Metrics saved to {metrics_path}")
    
    logger.info("=" * 60)
    logger.info("🎉 Training Complete!")
    logger.info("=" * 60)
    
    return best_model


if __name__ == "__main__":
    train_model()
