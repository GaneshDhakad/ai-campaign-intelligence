"""
Customer Segmentation Module
=============================
KMeans clustering with business-relevant segment profiling.
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


SEGMENT_PROFILES = {
    0: {"name": "Premium Champions", "icon": "👑", "color": "#FFD700",
        "strategy": "VIP treatment, exclusive offers, loyalty rewards, early access"},
    1: {"name": "Engaged Buyers", "icon": "🛒", "color": "#4CAF50",
        "strategy": "Cross-sell, upsell, personalized recommendations, referral programs"},
    2: {"name": "Potential Stars", "icon": "⭐", "color": "#2196F3",
        "strategy": "Onboarding campaigns, welcome discounts, product education"},
    3: {"name": "At-Risk", "icon": "⚠️", "color": "#F44336",
        "strategy": "Re-engagement campaigns, win-back offers, feedback surveys"}
}


class CustomerSegmenter:
    """KMeans-based customer segmentation with 4 business segments."""

    def __init__(self, n_clusters=4):
        self.n_clusters = n_clusters
        self.kmeans = None
        self.scaler = StandardScaler()
        self.segment_features = ['Income', 'CLV', 'Purchase_Frequency',
                                 'Engagement_Score', 'Recency']

    def fit(self, df: pd.DataFrame):
        """Fit segmentation model on customer data."""
        available = [c for c in self.segment_features if c in df.columns]
        if len(available) < 3:
            raise ValueError(f"Need at least 3 segmentation features, found: {available}")

        X = df[available].fillna(0)
        X_scaled = self.scaler.fit_transform(X)

        self.kmeans = KMeans(n_clusters=self.n_clusters, random_state=42, n_init=10)
        self.kmeans.fit(X_scaled)

        # Order clusters by CLV (highest = segment 0)
        if 'CLV' in available:
            clv_idx = available.index('CLV')
            center_clvs = self.kmeans.cluster_centers_[:, clv_idx]
            self._label_order = np.argsort(center_clvs)[::-1]
        else:
            self._label_order = np.arange(self.n_clusters)

        return self

    def predict(self, df: pd.DataFrame) -> np.ndarray:
        """Assign segment labels to customers."""
        available = [c for c in self.segment_features if c in df.columns]
        X = df[available].fillna(0)
        X_scaled = self.scaler.transform(X)
        raw_labels = self.kmeans.predict(X_scaled)

        # Remap to ordered labels
        label_map = {old: new for new, old in enumerate(self._label_order)}
        return np.array([label_map[l] for l in raw_labels])

    def get_segment_summary(self, df: pd.DataFrame) -> list:
        """Generate summary statistics per segment."""
        df = df.copy()
        available = [c for c in self.segment_features if c in df.columns]
        df['Segment'] = self.predict(df)

        summaries = []
        for seg_id in range(self.n_clusters):
            seg_df = df[df['Segment'] == seg_id]
            profile = SEGMENT_PROFILES.get(seg_id, {})

            summary = {
                'segment_id': seg_id,
                'name': profile.get('name', f'Segment {seg_id}'),
                'icon': profile.get('icon', '📊'),
                'color': profile.get('color', '#666'),
                'strategy': profile.get('strategy', 'N/A'),
                'count': len(seg_df),
                'pct': round(len(seg_df) / len(df) * 100, 1) if len(df) > 0 else 0,
                'metrics': {}
            }

            for col in available:
                if col in seg_df.columns:
                    summary['metrics'][col] = {
                        'mean': round(float(seg_df[col].mean()), 2),
                        'median': round(float(seg_df[col].median()), 2)
                    }

            summaries.append(summary)

        return summaries

    def predict_single(self, customer_data: dict) -> dict:
        """Predict segment for a single customer."""
        df = pd.DataFrame([customer_data])
        seg_id = int(self.predict(df)[0])
        profile = SEGMENT_PROFILES.get(seg_id, {})
        return {
            'segment_id': seg_id,
            'name': profile.get('name', f'Segment {seg_id}'),
            'icon': profile.get('icon', '📊'),
            'color': profile.get('color', '#666'),
            'strategy': profile.get('strategy', 'N/A')
        }
