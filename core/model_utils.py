"""
Core ML Module — AI Campaign Intelligence Engine
=================================================
Refactored production module for customer response prediction.
Includes SHAP explainability and cross-validation.
"""

import pandas as pd
import numpy as np
import pickle
import os
from datetime import datetime

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, classification_report
)
from imblearn.over_sampling import SMOTE

# =============================================================================
# PREPROCESSING
# =============================================================================

def preprocess_data(df, is_training=True):
    """Comprehensive data preprocessing pipeline."""
    df = df.copy()

    if 'Year_Birth' in df.columns:
        df = df[df['Year_Birth'] > 1900]

    if is_training and 'Response' in df.columns:
        target = df['Response']
        df.drop('Response', axis=1, inplace=True)
    else:
        target = None

    if 'ID' in df.columns:
        df.drop('ID', axis=1, inplace=True)

    df['Income'] = df['Income'].fillna(df['Income'].median())

    if 'Dt_Customer' in df.columns:
        df['Dt_Customer'] = pd.to_datetime(df['Dt_Customer'], dayfirst=True)
        reference_date = df['Dt_Customer'].max()
        df['Customer_Days'] = (reference_date - df['Dt_Customer']).dt.days
        df.drop('Dt_Customer', axis=1, inplace=True)

    constant_cols = [col for col in df.columns if df[col].nunique() == 1]
    if constant_cols:
        df.drop(constant_cols, axis=1, inplace=True)

    income_99 = df['Income'].quantile(0.99)
    df['Income'] = df['Income'].clip(upper=income_99)

    df['Age'] = 2014 - df['Year_Birth']
    df.drop('Year_Birth', axis=1, inplace=True)

    education_map = {'Basic': 1, '2n Cycle': 2, 'Graduation': 3, 'Master': 4, 'PhD': 5}
    df['Education'] = df['Education'].map(education_map)

    df['Is_Partnered'] = df['Marital_Status'].isin(['Married', 'Together']).astype(int)
    df.drop('Marital_Status', axis=1, inplace=True)

    return df, target


def engineer_features(df):
    """Create advanced behavioral and business features."""
    df = df.copy()

    spending_cols = ['MntWines', 'MntFruits', 'MntMeatProducts',
                     'MntFishProducts', 'MntSweetProducts', 'MntGoldProds']
    df['CLV'] = df[spending_cols].sum(axis=1)

    purchase_cols = ['NumDealsPurchases', 'NumWebPurchases',
                     'NumCatalogPurchases', 'NumStorePurchases']
    df['Purchase_Frequency'] = df[purchase_cols].sum(axis=1)

    df['Avg_Spending_Per_Purchase'] = df['CLV'] / (df['Purchase_Frequency'] + 1)

    purchase_score = (df['Purchase_Frequency'] / df['Purchase_Frequency'].max()) * 50
    web_visit_score = ((10 - df['NumWebVisitsMonth'].clip(upper=10)) / 10) * 50
    df['Engagement_Score'] = purchase_score + web_visit_score

    campaign_cols = ['AcceptedCmp1', 'AcceptedCmp2', 'AcceptedCmp3',
                     'AcceptedCmp4', 'AcceptedCmp5']
    df['Campaign_Acceptance_Rate'] = df[campaign_cols].sum(axis=1) / len(campaign_cols)

    df['Total_Dependents'] = df['Kidhome'] + df['Teenhome']
    df['Income_Per_Member'] = df['Income'] / (df['Total_Dependents'] + df['Is_Partnered'] + 1)
    df['Recency_Risk'] = df['Recency'] / df['Recency'].max()

    channel_cols = ['NumWebPurchases', 'NumCatalogPurchases', 'NumStorePurchases']
    df['Channel_Diversity'] = (df[channel_cols] > 0).sum(axis=1)
    df['Product_Diversity'] = (df[spending_cols] > 0).sum(axis=1)

    return df


# =============================================================================
# TRAINING
# =============================================================================

def train_models(X_train, y_train, X_test, y_test):
    """Train and evaluate multiple models, return best."""
    models = {}
    results = []

    print("  Training Logistic Regression...")
    lr = LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced')
    lr.fit(X_train, y_train)
    models['Logistic Regression'] = lr

    print("  Training Random Forest...")
    rf = RandomForestClassifier(n_estimators=200, max_depth=10, min_samples_split=5,
                                random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    models['Random Forest'] = rf

    print("  Training XGBoost...")
    xgb = XGBClassifier(n_estimators=300, learning_rate=0.1, max_depth=5,
                        subsample=0.8, colsample_bytree=0.8, random_state=42,
                        eval_metric='logloss')
    xgb.fit(X_train, y_train)
    models['XGBoost'] = xgb

    for name, model in models.items():
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]
        results.append({
            'Model': name,
            'Accuracy': round(accuracy_score(y_test, y_pred), 4),
            'Precision': round(precision_score(y_test, y_pred), 4),
            'Recall': round(recall_score(y_test, y_pred), 4),
            'F1-Score': round(f1_score(y_test, y_pred), 4),
            'ROC-AUC': round(roc_auc_score(y_test, y_proba), 4)
        })

    return models, pd.DataFrame(results)


# =============================================================================
# PREDICTION
# =============================================================================

def predict_with_recommendation(input_data, model, scaler, feature_columns):
    """Make prediction with business recommendations."""
    input_df = pd.DataFrame([input_data])
    for col in feature_columns:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = input_df[feature_columns]
    input_scaled = scaler.transform(input_df)

    probability = model.predict_proba(input_scaled)[0][1]
    prediction = "Will Respond" if probability > 0.5 else "Will Not Respond"

    if probability >= 0.75:
        risk_level, recommendation, action, color = (
            "High Probability",
            "✅ Prime Target: Include in premium campaigns with personalized offers",
            "Target", "high-prob"
        )
    elif probability >= 0.5:
        risk_level, recommendation, action, color = (
            "Medium Probability",
            "⚠️ Potential Responder: Include in standard campaigns with incentives",
            "Engage", "medium-prob"
        )
    elif probability >= 0.25:
        risk_level, recommendation, action, color = (
            "Low Probability",
            "🔄 At-Risk: Re-engagement campaign with discount offers",
            "Re-engage", "low-prob"
        )
    else:
        risk_level, recommendation, action, color = (
            "Very Low Probability",
            "❌ Low Priority: Exclude from expensive campaigns",
            "Deprioritize", "low-prob"
        )

    return {
        'prediction': prediction,
        'probability': round(probability * 100, 2),
        'probability_raw': float(probability),
        'risk_level': risk_level,
        'recommendation': recommendation,
        'action': action,
        'color': color
    }


# =============================================================================
# PERSISTENCE
# =============================================================================

def save_model_artifacts(model, scaler, feature_columns, model_name="best_model", filename=None):
    """Save trained model and preprocessing artifacts."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    artifacts = {
        'model': model, 'scaler': scaler, 'feature_columns': feature_columns,
        'model_name': model_name, 'timestamp': timestamp
    }
    if filename is None:
        filename = f"artifacts/model_artifacts_{timestamp}.pkl"
    with open(filename, 'wb') as f:
        pickle.dump(artifacts, f)
    print(f"  ✓ Model saved: {filename}")
    return filename


def load_model_artifacts(filename):
    """Load saved model artifacts."""
    with open(filename, 'rb') as f:
        artifacts = pickle.load(f)
    print(f"  ✓ Loaded: {artifacts['model_name']} (saved {artifacts['timestamp']})")
    return artifacts


# =============================================================================
# PRODUCTION CLASS
# =============================================================================

class CustomerResponsePredictor:
    """Production customer response prediction system with SHAP support."""

    def __init__(self):
        self.model = None
        self.scaler = None
        self.feature_columns = None
        self.model_name = None
        self._shap_explainer = None

    def preprocess(self, df, is_training=True):
        return preprocess_data(df, is_training)

    def engineer_features(self, df):
        return engineer_features(df)

    def train(self, X_train, y_train, X_test, y_test, use_smote=True):
        if use_smote:
            print("  Applying SMOTE...")
            smote = SMOTE(random_state=42, k_neighbors=5)
            X_train, y_train = smote.fit_resample(X_train, y_train)
            print(f"  ✓ Balanced samples: {X_train.shape[0]}")

        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        if isinstance(X_train, pd.DataFrame):
            self.feature_columns = X_train.columns.tolist()
        else:
            self.feature_columns = [f"feature_{i}" for i in range(X_train.shape[1])]

        models, performance = train_models(X_train_scaled, y_train, X_test_scaled, y_test)

        best_name = performance.sort_values('ROC-AUC', ascending=False).iloc[0]['Model']
        self.model = models[best_name]
        self.model_name = best_name
        self._shap_explainer = None  # reset

        # Cross-validation on best model
        cv_scores = cross_val_score(self.model, X_train_scaled, y_train, cv=5, scoring='roc_auc')
        print(f"\n  🏆 Best: {best_name} | CV ROC-AUC: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

        return performance

    def predict(self, input_data):
        if self.model is None:
            raise ValueError("Model not loaded.")
        return predict_with_recommendation(input_data, self.model, self.scaler, self.feature_columns)

    def predict_batch(self, input_df):
        if self.model is None:
            raise ValueError("Model not loaded.")
        results = []
        for idx, row in input_df.iterrows():
            result = self.predict(row.to_dict())
            result['customer_id'] = idx
            results.append(result)
        return pd.DataFrame(results)

    def get_shap_values(self, input_data):
        """Get SHAP values for a single prediction."""
        try:
            import shap
        except ImportError:
            return None

        if self._shap_explainer is None:
            self._shap_explainer = shap.TreeExplainer(self.model)

        input_df = pd.DataFrame([input_data])
        for col in self.feature_columns:
            if col not in input_df.columns:
                input_df[col] = 0
        input_df = input_df[self.feature_columns]
        input_scaled = self.scaler.transform(input_df)

        shap_values = self._shap_explainer.shap_values(input_scaled)

        # Handle multi-output (binary)
        if isinstance(shap_values, list):
            sv = shap_values[1][0]  # class 1 (respond)
        else:
            sv = shap_values[0]

        feature_impacts = sorted(
            zip(self.feature_columns, sv),
            key=lambda x: abs(x[1]), reverse=True
        )

        return {
            'shap_values': dict(feature_impacts),
            'base_value': float(self._shap_explainer.expected_value[1]
                                if isinstance(self._shap_explainer.expected_value, (list, np.ndarray))
                                else self._shap_explainer.expected_value),
            'feature_names': self.feature_columns,
            'raw_shap': sv.tolist()
        }

    def get_feature_importance(self):
        """Get model feature importance."""
        if hasattr(self.model, 'feature_importances_'):
            imp = sorted(
                zip(self.feature_columns, self.model.feature_importances_),
                key=lambda x: x[1], reverse=True
            )
            return {name: round(float(val), 4) for name, val in imp}
        return {}

    def save(self, filename='artifacts/model_artifacts.pkl'):
        if self.model is None:
            raise ValueError("No model to save.")
        return save_model_artifacts(self.model, self.scaler, self.feature_columns,
                                   self.model_name, filename)

    def load(self, filename='artifacts/model_artifacts.pkl'):
        artifacts = load_model_artifacts(filename)
        self.model = artifacts['model']
        self.scaler = artifacts['scaler']
        self.feature_columns = artifacts['feature_columns']
        self.model_name = artifacts['model_name']
        self._shap_explainer = None
