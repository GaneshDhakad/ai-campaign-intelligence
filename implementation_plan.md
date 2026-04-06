# AI Campaign Intelligence Engine — Production Transformation Plan

## Goal
Transform the current Minor2 prototype into a **premium, production-grade SaaS product** with a FastAPI backend, a stunning Streamlit dark-theme dashboard, SHAP explainability, VADER-enhanced NLP, SQLite persistence, batch prediction, campaign simulation, and deployment-ready architecture.

---

## User Review Required

> [!IMPORTANT]
> **Architecture Choice**: This plan uses **FastAPI** as the backend API layer and keeps **Streamlit** as the frontend dashboard (communicating via REST). This gives you clean separation of concerns while staying within your existing tech stack. If you prefer a fully custom HTML/JS frontend instead, let me know before I proceed.

> [!IMPORTANT]
> **NLP Upgrade**: I'll use **VADER** (rule-based, no GPU needed, instant results) instead of BERT/DistilBERT. VADER provides sentiment intensity scores (compound, pos, neg, neu) and is production-proven for social media/review text. BERT would require PyTorch (~2GB), a GPU for reasonable speed, and adds deployment complexity that isn't justified for this use case. If you specifically want BERT, let me know.

> [!WARNING]
> **Database**: I'll use **SQLite** (zero-config, file-based, perfect for portfolio demos). PostgreSQL is overkill until you have concurrent multi-user load. The schema will be designed so migration to PostgreSQL is trivial later.

---

## Proposed Architecture

```
Minor2/
├── backend/                          # FastAPI Backend (API Layer)
│   ├── __init__.py
│   ├── main.py                       # FastAPI app, CORS, lifespan
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── predict.py                # /predict, /batch_predict
│   │   ├── sentiment.py              # /sentiment
│   │   ├── analytics.py              # /analytics, /segments, /simulation
│   │   └── health.py                 # /health
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ml_service.py             # ML prediction logic (wraps model_utils)
│   │   ├── nlp_service.py            # NLP sentiment logic (VADER + TF-IDF)
│   │   ├── analytics_service.py      # Segmentation, simulation, ROI
│   │   └── db_service.py             # SQLite CRUD operations
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py                # Pydantic request/response models
│   └── database/
│       ├── __init__.py
│       ├── connection.py             # SQLite connection manager
│       └── migrations.py             # Schema creation
│
├── frontend/                         # Streamlit Frontend (Dashboard)
│   ├── app.py                        # Main Streamlit entry point
│   ├── pages/
│   │   ├── 1_🎯_Predict.py           # Individual prediction page
│   │   ├── 2_📦_Batch_Predict.py     # CSV upload batch prediction
│   │   ├── 3_💬_Sentiment.py         # Sentiment analysis page
│   │   ├── 4_📊_Analytics.py         # Historical analytics dashboard
│   │   ├── 5_🧪_Simulator.py         # Campaign what-if simulator
│   │   └── 6_👥_Segments.py          # Customer segmentation view
│   ├── components/
│   │   ├── __init__.py
│   │   ├── sidebar.py                # Sidebar control panel
│   │   ├── kpi_cards.py              # Premium KPI card components
│   │   ├── charts.py                 # Plotly chart builders
│   │   └── theme.py                  # CSS theme and styling
│   └── assets/
│       └── logo.png                  # Brand logo (generated)
│
├── core/                             # Shared ML/NLP Logic
│   ├── __init__.py
│   ├── model_utils.py                # Refactored from current model_utils.py
│   ├── sentiment_engine.py           # VADER + TF-IDF hybrid sentiment
│   ├── explainer.py                  # SHAP explainability module
│   └── segmentation.py              # KMeans customer segmentation
│
├── data/
│   ├── marketing_campaign.csv
│   ├── Reviews.csv
│   └── campaign_engine.db            # SQLite database (generated)
│
├── artifacts/                        # Trained model files
│   ├── model_artifacts.pkl
│   └── nlp_artifacts.pkl
│
├── scripts/
│   └── train.py                      # Standalone training script
│
├── requirements.txt                  # Updated dependencies
├── README.md                         # Updated documentation
└── .env                              # Environment config (optional)
```

---

## Proposed Changes (by Phase)

### Phase 1: Foundation & Backend (Priority: HIGHEST)

#### [NEW] requirements.txt
- Add: `fastapi`, `uvicorn[standard]`, `vaderSentiment`, `pydantic`, `httpx`, `aiosqlite`
- Keep all existing ML dependencies

---

#### [NEW] core/model_utils.py
- Move and refactor from root `model_utils.py`
- Add SHAP explainability method to `CustomerResponsePredictor`
- Add confidence interval calculation
- Add cross-validation scoring method

#### [NEW] core/sentiment_engine.py
- Hybrid VADER + TF-IDF sentiment engine
- Returns: compound score, confidence, intensity breakdown (pos/neg/neu), keywords
- Falls back to TF-IDF model when VADER is neutral

#### [NEW] core/explainer.py
- SHAP TreeExplainer for XGBoost
- Methods: `get_shap_values()`, `get_feature_importance()`, `explain_single()`
- Cached explainer instance for performance

#### [NEW] core/segmentation.py
- KMeans clustering (4 segments)
- Segment profiling and naming
- Segment assignment for new customers

---

#### [NEW] backend/main.py
- FastAPI app with CORS middleware
- Lifespan event to load models on startup
- Mount all route modules

#### [NEW] backend/routes/predict.py
- `POST /predict` — Single customer prediction + SHAP explanation
- `POST /batch_predict` — CSV upload, returns predictions as JSON/CSV
- Both endpoints persist results to SQLite

#### [NEW] backend/routes/sentiment.py
- `POST /sentiment` — Analyze text, return compound score + keywords + confidence

#### [NEW] backend/routes/analytics.py
- `GET /analytics/summary` — Historical prediction stats
- `GET /analytics/segments` — Customer segment distribution
- `POST /analytics/simulate` — Campaign what-if simulation

#### [NEW] backend/routes/health.py
- `GET /health` — System health check (model loaded, DB connected)

#### [NEW] backend/models/schemas.py
- Pydantic models for all request/response types
- Strict validation with field descriptions

#### [NEW] backend/database/connection.py
- SQLite connection manager with context manager pattern
- Thread-safe connection pooling

#### [NEW] backend/database/migrations.py
- Schema: `predictions`, `sentiment_results`, `batch_jobs` tables
- Auto-create on first run

---

### Phase 2: Premium Frontend (Priority: HIGH)

#### [NEW] frontend/app.py
- Dark SaaS theme with glassmorphism
- Hero section with animated KPI cards
- Navigation via Streamlit multi-page architecture

#### [NEW] frontend/components/theme.py
- 300+ lines of custom CSS
- Dark mode palette (#0f0f23, #1a1a2e, #16213e)
- Glassmorphism cards (backdrop-filter: blur, rgba backgrounds)
- Animated counters, hover effects, gradient borders
- Custom fonts (Inter via Google Fonts)

#### [NEW] frontend/components/kpi_cards.py
- Animated metric cards with delta indicators
- Color-coded by status (green/amber/red)
- Sparkline mini-charts inside cards

#### [NEW] frontend/components/charts.py
- Dark-themed Plotly charts
- Gauge chart, radar chart, waterfall chart (SHAP)
- Animated bar charts for feature importance

#### [NEW] frontend/pages/1_🎯_Predict.py
- Premium prediction interface
- Real-time SHAP waterfall chart
- Confidence indicator with animated ring
- Sentiment-adjusted recommendation panel

#### [NEW] frontend/pages/2_📦_Batch_Predict.py
- CSV upload with drag-and-drop
- Progress bar during processing
- Download results as CSV
- Summary statistics after batch

#### [NEW] frontend/pages/3_💬_Sentiment.py
- Large text input area
- Real-time sentiment gauge (compound score)
- Keyword highlighting (positive/negative words)
- Sentiment intensity breakdown (pos/neg/neu bars)

#### [NEW] frontend/pages/4_📊_Analytics.py
- Historical prediction trends (line chart)
- Response rate over time
- Segment distribution (donut chart)
- Top features driving predictions (SHAP summary)

#### [NEW] frontend/pages/5_🧪_Simulator.py
- Campaign what-if sliders
- ROI prediction based on segment targeting
- Before/after comparison charts
- Budget allocation optimizer

#### [NEW] frontend/pages/6_👥_Segments.py
- 4-segment overview cards
- Scatter plot (CLV vs Engagement, colored by segment)
- Segment drill-down with customer lists
- Recommended strategy per segment

---

### Phase 3: Data & Persistence (Priority: MEDIUM)

#### [NEW] data/campaign_engine.db (auto-generated)
- Tables:
  - `predictions` (id, timestamp, input_json, prediction, probability, sentiment, recommendation)
  - `batch_jobs` (id, timestamp, filename, total_records, avg_probability)
  - `sentiment_logs` (id, timestamp, text, compound_score, pos, neg, neu)

---

### Phase 4: Polish & Deploy (Priority: LOWER)

#### [MODIFY] README.md
- Architecture diagram (Mermaid)
- API documentation
- Deployment instructions (Render, Railway, AWS)
- Screenshots of the premium dashboard

#### [NEW] scripts/train.py
- Standalone training with progress output
- Trains both ML and NLP models
- Saves to `artifacts/` directory

---

## Execution Priority Order

| Priority | Phase | What | Est. Time |
|----------|-------|------|-----------|
| 1 | **Foundation** | Install deps, restructure directories, move `model_utils.py` to `core/` | 10 min |
| 2 | **Backend** | FastAPI app + all REST endpoints + SQLite | 30 min |
| 3 | **Core ML** | SHAP explainer, VADER sentiment, segmentation | 20 min |
| 4 | **Frontend Theme** | Dark CSS, glassmorphism, KPI cards, chart builders | 25 min |
| 5 | **Frontend Pages** | All 6 pages with premium UI | 40 min |
| 6 | **Integration** | Connect frontend → backend via `httpx` | 15 min |
| 7 | **Training** | Retrain models with updated pipeline | 5 min |
| 8 | **Polish** | README, final testing, screenshots | 10 min |

---

## Open Questions

> [!IMPORTANT]
> 1. **VADER vs BERT**: Confirmed using VADER for speed and simplicity. Override?
> 2. **Frontend-Backend Communication**: The Streamlit pages will call FastAPI via `httpx`. Both run locally (Streamlit on 8501, FastAPI on 8000). Acceptable?
> 3. **Logo/Branding**: I'll generate a professional logo for "AI Campaign Intelligence Engine" using the image generation tool. Any color/style preferences?

## Verification Plan

### Automated Tests
- `python -m pytest backend/` — API endpoint tests
- `curl http://localhost:8000/health` — Health check
- `curl -X POST http://localhost:8000/predict -d '{...}'` — Prediction endpoint

### Manual Verification
- Launch both servers and verify all 6 pages render correctly
- Test batch upload with a sample CSV
- Verify SQLite persistence by checking stored predictions
- Confirm SHAP waterfall chart renders for individual predictions
