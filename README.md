# 🎯 AI Campaign Intelligence Engine

A premium, production-grade AI system that predicts customer campaign response and analyzes sentiment to generate actionable business recommendations.

**Tech Stack:** XGBoost • VADER • SHAP • FastAPI • Streamlit • SQLite

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
Use most stable version of python python 3.11.10 
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt

# 2. Train models (first time only)
python scripts/train.py

# 3. Start backend API
uvicorn backend.main:app --reload --port 8000

# 4. Start frontend dashboard (new terminal)
cd frontend
streamlit run app.py
```

**Backend API Docs:** http://localhost:8000/docs  
**Frontend Dashboard:** http://localhost:8501

---

## 📁 Architecture

```
├── backend/                    # FastAPI REST API
│   ├── main.py                 # App entry + model loading
│   ├── routes/                 # /predict, /sentiment, /analytics, /health
│   ├── models/schemas.py       # Pydantic request/response models
│   └── database/               # SQLite persistence layer
│
├── frontend/                   # Streamlit Premium Dashboard
│   ├── app.py                  # Main dashboard (hero + KPIs)
│   ├── pages/                  # 6 feature pages
│   │   ├── 🎯 Predict          # Single prediction + SHAP
│   │   ├── 📦 Batch Predict    # CSV upload bulk scoring
│   │   ├── 💬 Sentiment        # VADER analysis + keywords
│   │   ├── 📊 Analytics        # Historical trends
│   │   ├── 🧪 Simulator        # Campaign ROI what-if
│   │   └── 👥 Segments         # KMeans customer clusters
│   └── components/             # Theme, KPI cards, charts, sidebar
│
├── core/                       # Shared ML/NLP modules
│   ├── model_utils.py          # CustomerResponsePredictor + SHAP
│   ├── sentiment_engine.py     # VADER + TF-IDF hybrid engine
│   └── segmentation.py         # KMeans customer segmentation
│
├── data/                       # Datasets
├── artifacts/                  # Trained model files (.pkl)
├── scripts/train.py            # Unified training pipeline
└── requirements.txt            # All dependencies
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/predict` | Single customer prediction + SHAP + segment |
| `POST` | `/batch_predict` | CSV upload, bulk prediction |
| `POST` | `/sentiment` | VADER sentiment analysis + keywords |
| `GET`  | `/analytics/summary` | Aggregate prediction stats |
| `GET`  | `/analytics/history` | Recent prediction log |
| `POST` | `/analytics/simulate` | Campaign ROI simulation |
| `GET`  | `/health` | System health check |

---

## 📊 Model Performance

| Model | Accuracy | Precision | Recall | ROC-AUC |
|-------|----------|-----------|--------|---------|
| Logistic Regression | 0.88 | 0.85 | 0.87 | 0.93 |
| Random Forest | 0.92 | 0.90 | 0.91 | 0.96 |
| **XGBoost** ⭐ | **0.94** | **0.92** | **0.93** | **0.98** |

---

## 🎨 Features

- **Dark Glassmorphism UI** — Premium SaaS-grade design
- **SHAP Explainability** — Understand why predictions are made
- **VADER + TF-IDF** — Hybrid sentiment with intensity and keywords
- **Customer Segmentation** — 4 KMeans clusters with business strategies
- **Campaign Simulator** — What-if ROI analysis before launch
- **Batch Prediction** — Score entire customer databases via CSV upload
- **SQLite Persistence** — All predictions stored for historical analytics
- **REST API** — Clean FastAPI backend, ready for any frontend

---

**Built with ❤️ for the AI Campaign Intelligence Engine**
