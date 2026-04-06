"""
Hybrid Sentiment Engine — VADER + TF-IDF
=========================================
Uses VADER for real-time intensity scores and TF-IDF+LR for classification.
"""

import pickle
import os
import pandas as pd
import numpy as np
from datetime import datetime

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


class SentimentEngine:
    """
    Hybrid sentiment analysis combining VADER (intensity) and TF-IDF+LR (classification).
    
    VADER provides:  compound score, pos/neg/neu breakdown, intensity
    TF-IDF+LR provides:  trained label classification (1, 0, -1)
    Combined:  best of both worlds
    """

    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()
        self.tfidf = None
        self.lr_model = None
        self.is_trained = False

    def train(self, data_path='data/Reviews.csv', max_chunks=2):
        """Train TF-IDF + Logistic Regression on review data."""
        print("  Training Sentiment Engine (TF-IDF + LR)...")
        chunks = pd.read_csv(data_path, chunksize=20000)
        df_text = pd.concat(
            [chunk[["Text", "Score"]] for i, chunk in enumerate(chunks) if i < max_chunks]
        )
        df_text.dropna(inplace=True)

        def label(score):
            if score >= 4: return 1
            elif score == 3: return 0
            else: return -1

        df_text["Sentiment"] = df_text["Score"].apply(label)

        self.tfidf = TfidfVectorizer(max_features=5000, stop_words="english")
        X = self.tfidf.fit_transform(df_text["Text"])
        y = df_text["Sentiment"]

        self.lr_model = LogisticRegression(max_iter=300, random_state=42)
        self.lr_model.fit(X, y)
        self.is_trained = True
        print("  ✓ Sentiment Engine trained")

    def analyze(self, text: str) -> dict:
        """
        Full sentiment analysis.
        
        Returns:
            dict with: label, compound, confidence, pos, neg, neu,
                       intensity, keywords
        """
        # VADER scores
        vs = self.vader.polarity_scores(text)
        compound = vs['compound']
        pos, neg, neu = vs['pos'], vs['neg'], vs['neu']

        # VADER-based label
        if compound >= 0.05:
            vader_label = 1
        elif compound <= -0.05:
            vader_label = -1
        else:
            vader_label = 0

        # TF-IDF classification (if trained)
        tfidf_label = None
        tfidf_confidence = 0.0
        if self.is_trained and self.tfidf and self.lr_model:
            vec = self.tfidf.transform([text])
            tfidf_label = int(self.lr_model.predict(vec)[0])
            proba = self.lr_model.predict_proba(vec)[0]
            tfidf_confidence = float(max(proba))

        # Hybrid: prefer VADER when strong signal, TF-IDF for nuance
        if abs(compound) >= 0.3:
            final_label = vader_label
            confidence = min(abs(compound) * 1.2, 1.0)
        elif tfidf_label is not None:
            final_label = tfidf_label
            confidence = tfidf_confidence
        else:
            final_label = vader_label
            confidence = abs(compound)

        # Intensity classification
        abs_comp = abs(compound)
        if abs_comp >= 0.6:
            intensity = "Strong"
        elif abs_comp >= 0.3:
            intensity = "Moderate"
        elif abs_comp >= 0.05:
            intensity = "Mild"
        else:
            intensity = "Neutral"

        # Extract influential keywords
        keywords = self._extract_keywords(text)

        label_text = {1: "Positive", 0: "Neutral", -1: "Negative"}

        return {
            'label': final_label,
            'label_text': label_text.get(final_label, "Unknown"),
            'compound': round(compound, 4),
            'confidence': round(confidence, 4),
            'pos': round(pos, 4),
            'neg': round(neg, 4),
            'neu': round(neu, 4),
            'intensity': intensity,
            'keywords': keywords,
            'vader_label': vader_label,
            'tfidf_label': tfidf_label,
            'tfidf_confidence': round(tfidf_confidence, 4) if tfidf_label is not None else None
        }

    def _extract_keywords(self, text: str) -> dict:
        """Extract positive and negative keywords from text."""
        words = text.lower().split()
        positive_words = []
        negative_words = []

        for word in words:
            clean = ''.join(c for c in word if c.isalpha())
            if not clean or len(clean) < 3:
                continue
            score = self.vader.polarity_scores(clean)['compound']
            if score >= 0.3:
                positive_words.append(clean)
            elif score <= -0.3:
                negative_words.append(clean)

        return {
            'positive': list(set(positive_words))[:10],
            'negative': list(set(negative_words))[:10]
        }

    def save(self, filename='artifacts/nlp_artifacts.pkl'):
        """Save trained TF-IDF + LR artifacts."""
        if not self.is_trained:
            raise ValueError("Engine not trained.")
        artifacts = {
            'tfidf': self.tfidf,
            'lr_model': self.lr_model,
            'timestamp': datetime.now().strftime("%Y%m%d_%H%M%S")
        }
        with open(filename, 'wb') as f:
            pickle.dump(artifacts, f)
        print(f"  ✓ NLP artifacts saved: {filename}")

    def load(self, filename='artifacts/nlp_artifacts.pkl'):
        """Load trained TF-IDF + LR artifacts."""
        with open(filename, 'rb') as f:
            artifacts = pickle.load(f)
        self.tfidf = artifacts.get('tfidf') or artifacts.get('tfidf')
        self.lr_model = artifacts.get('lr_model') or artifacts.get('model')
        self.is_trained = self.tfidf is not None and self.lr_model is not None
        print(f"  ✓ NLP artifacts loaded")
