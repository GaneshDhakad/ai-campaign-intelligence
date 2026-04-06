"""
Unified Training Script — AI Campaign Intelligence Engine
==========================================================
Trains both ML (XGBoost) and NLP (VADER + TF-IDF) models.

Usage:
    python scripts/train.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
from sklearn.model_selection import train_test_split
from core.model_utils import CustomerResponsePredictor
from core.sentiment_engine import SentimentEngine


def main():
    print("=" * 60)
    print("🚀 AI Campaign Intelligence Engine — Training Pipeline")
    print("=" * 60)

    os.makedirs('artifacts', exist_ok=True)

    # ── 1. Marketing Response Model ──
    print("\n📊 Phase 1: Marketing Response Model")
    print("-" * 40)
    try:
        predictor = CustomerResponsePredictor()
        df = pd.read_csv('data/marketing_campaign.csv', sep='\t')
        print(f"  Loaded {len(df)} records")

        df_clean, y = predictor.preprocess(df)
        df_features = predictor.engineer_features(df_clean)
        print(f"  Engineered {len(df_features.columns)} features")

        X_train, X_test, y_train, y_test = train_test_split(
            df_features, y, test_size=0.2, random_state=42, stratify=y
        )

        performance = predictor.train(X_train, y_train, X_test, y_test)
        print("\n  📋 Model Performance:")
        print(performance.to_string(index=False))

        predictor.save('artifacts/model_artifacts.pkl')
    except Exception as e:
        print(f"  ✗ ML Training Failed: {e}")
        import traceback
        traceback.print_exc()

    # ── 2. NLP Sentiment Engine ──
    print("\n\n💬 Phase 2: NLP Sentiment Engine")
    print("-" * 40)
    try:
        engine = SentimentEngine()
        reviews_path = 'data/Reviews.csv'
        if os.path.exists(reviews_path):
            engine.train(reviews_path)
            engine.save('artifacts/nlp_artifacts.pkl')

            # Quick test
            test_texts = [
                "Amazing product, absolutely love it!",
                "Terrible quality, waste of money",
                "The product is decent, nothing special"
            ]
            print("\n  🧪 Quick Sentiment Test:")
            for t in test_texts:
                r = engine.analyze(t)
                print(f"    {r['label_text']:>8} ({r['compound']:+.3f}) | \"{t[:50]}\"")
        else:
            print(f"  ✗ {reviews_path} not found, skipping NLP")
    except Exception as e:
        print(f"  ✗ NLP Training Failed: {e}")

    print("\n" + "=" * 60)
    print("✅ Training Pipeline Complete")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Start backend:  uvicorn backend.main:app --reload --port 8000")
    print("  2. Start frontend: streamlit run frontend/app.py")


if __name__ == "__main__":
    main()
