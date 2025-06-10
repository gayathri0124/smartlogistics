# 🚛 SmartLogistics

**SmartLogistics** is an AI-powered logistics intelligence platform built with Streamlit. It enables real-time shipment tracking, predictive delay analytics, route optimization, and performance evaluation—all without requiring a database. The platform uses mock data and integrates LLM-based analysis for smarter insights.

![App Screenshot](generated-icon.png)

---

## 🔧 Features

- **📍 Shipment Tracking** — Track individual shipments with dynamic filters, mapping, and AI status analysis
- **🔮 Delay Predictions** — Predict delays using a custom model and receive actionable LLM-based insights
- **🗺️ Route Optimization** — Optimize delivery routes and visualize them with Folium + AI suggestions
- **📊 Performance Analytics** — Visual KPIs, weather impact, historical trends, and downloadable reports
- **📤 Notification Settings** — JSON-configured mock alert preferences for email/SMS/weather

---

## 📁 Project Structure

smartlogistics/
├── .streamlit/ # Streamlit config
├── app.py # App entry point
├── check_env.py # Environment checks
├── data/
│ ├── notifications/
│ │ └── demo_user.json # Notification preferences
│ └── mock_shipments.py # Generates mock shipment data
├── pages/ # Streamlit multi-page setup
│ ├── 1_shipment_tracking.py
│ ├── 2_predictions.py
│ ├── 3_route_optimization.py
│ └── 4_analytics.py
├── utils/ # Reusable helper modules
│ ├── data_utils.py
│ ├── export_utils.py
│ ├── llm_utils.py
│ ├── ml_utils.py
│ ├── notification_utils.py
│ ├── viz_utils.py
│ └── weather_utils.py
├── generated-icon.png # Custom icon (optional)
├── README.md
├── pyproject.toml # Dependency definitions
└── uv.lock # Poetry lock file

---

## ⚙️ Getting Started

### ✅ Prerequisites

- Python 3.8+
- [Poetry](https://python-poetry.org/docs/#installation) for dependency management *(or use pip manually)*

### 🚀 Setup

1. **Clone the repository**

```bash
git clone https://github.com/gayathri0124/smartlogistics.git
cd smartlogistics
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the streamlit app

```bash
streamlit run app.py
```

---

## 🧪 Demo Flow

| Page               | Purpose                                                                 |
|--------------------|-------------------------------------------------------------------------|
| **Shipment Tracking** | Visual tracking with search, filters, and AI-based risk/status analysis     |
| **Delay Predictions** | Predict shipment delays and visualize delay distribution + insights       |
| **Route Optimization**| Select optimal routes, add waypoints, view interactive maps, get LLM advice |
| **Analytics**         | KPI dashboard with weather trends, route efficiency, and downloadable reports |

---

## 🧠 AI & ML Components

- **`DelayPredictor`**  
  Custom ML model estimating shipment delay using distance, weather, and time data.

- **`llm_utils.py`**  
  Simulates LLM-driven reasoning for risk detection and routing recommendations.

- **`create_shipment_map`**  
  Generates interactive Folium-based shipment maps with path visualization.
