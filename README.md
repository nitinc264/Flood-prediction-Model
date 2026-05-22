# 🌊 RiskRadar — Flood Risk Prediction System

> **An End-to-End Machine Learning System for Flood Risk Prediction using Hydrological, Meteorological, and Geospatial Data.**  
> Built using **XGBoost**, deployed with **FastAPI**, and visualized through an interactive **Streamlit Dashboard**.

---

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python)
![XGBoost](https://img.shields.io/badge/XGBoost-2.0-orange?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green?style=for-the-badge&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red?style=for-the-badge&logo=streamlit)
![Accuracy](https://img.shields.io/badge/Accuracy-96.9%25-brightgreen?style=for-the-badge)
![F1 Score](https://img.shields.io/badge/F1%20Score-0.984-brightgreen?style=for-the-badge)

---

# 📌 Table of Contents

- [📖 Overview](#-overview)
- [✨ Key Features](#-key-features)
- [🧠 Model & Methodology](#-model--methodology)
- [📊 Results](#-results)
- [🏗️ Project Structure](#️-project-structure)
- [⚙️ Installation](#️-installation)
- [🚀 Running the Project](#-running-the-project)
- [🔌 API Reference](#-api-reference)
- [🐳 Docker Support](#-docker-support)
- [🛠️ Tech Stack](#️-tech-stack)
- [📈 Future Scope](#-future-scope)
- [📜 License](#-license)
- [👨‍💻 Author](#-author)

---

# 📖 Overview

RiskRadar is a production-grade flood risk prediction system that analyzes hydrological, meteorological, and geospatial parameters to classify locations into flood risk categories.

The project leverages a high-performance **XGBoost Machine Learning model** trained on real-world flood datasets and provides predictions through:

- 🚀 FastAPI REST API
- 📊 Interactive Streamlit Dashboard
- 🐳 Dockerized Deployment Pipeline

Unlike a traditional ML notebook project, RiskRadar focuses on a complete deployment-ready architecture suitable for real-world usage.

---

# ✨ Key Features

✅ Trained on **45,932 global flood locations**  
✅ Achieved **96.9% Accuracy**  
✅ **F1 Score: 0.984**  
✅ Uses **SMOTE** for class imbalance handling  
✅ Real-time prediction dashboard with Plotly visualizations  
✅ FastAPI backend with input validation  
✅ Interactive flood-risk mapping  
✅ Docker-ready deployment  
✅ Production-oriented ML workflow

---

# 🧠 Model & Methodology

## 📂 Dataset

- **Source:** IIT Delhi Static Flood Database
- **Dataset File:** `kuntla_flooddatabase.csv`
- **Raw Features:** 93
- **Final Engineered Features:** 13
- **Target:** Flood Risk Classification

---

## 🔄 Machine Learning Pipeline

```text
Raw Dataset (93 Parameters)
        ↓
Missing Value Handling
        ↓
Feature Engineering
        ↓
Categorical Encoding
        ↓
Train/Test Split
        ↓
SMOTE Balancing
        ↓
Hyperparameter Tuning
        ↓
XGBoost Training
        ↓
Evaluation & Model Export
        ↓
FastAPI + Streamlit Deployment
```

---

## ⚙️ Data Preprocessing

### Missing Value Handling
- Dropped columns with more than 40% missing values
- Median imputation for numerical features

### Feature Engineering
Created custom engineered features such as:
- `precipitation_risk_index`
- `drainage_risk_index`

### Encoding
Applied Label Encoding for:
- Climate Type
- Landcover Type
- Soil Type
- Lithology Type

---

## 🤖 Model Training

### Algorithm Used
- **XGBoost Classifier**

### Hyperparameter Optimization
- `RandomizedSearchCV`
- 50 parameter combinations
- 3-fold cross-validation
- GPU accelerated training (`tree_method=hist`)

### Handling Imbalanced Data
- Applied **SMOTE** on training dataset

---

# 📊 Results

| Metric | Score |
|---|---|
| Accuracy | 96.9% |
| F1 Score | 0.984 |
| Recall | 0.791 |

---

## 🌍 High Risk Locations

- High-risk locations identified: **2,538**
- Total locations analyzed: **45,932**

---

## 🔥 Most Important Risk Factors

- Annual Precipitation
- Seasonal Rainfall Patterns
- Drainage Density
- Basin Relief
- Soil Characteristics
- Land Cover Features
- Temperature Seasonality

---

# 🏗️ Project Structure

```bash
riskradar/
│
├── flood_fast.py
├── api.py
├── app.py
├── Dockerfile
├── requirements.txt
├── flood_model.pkl
├── encoders.pkl
├── feature_columns.pkl
├── high_risk_locations.csv
└── README.md
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/nitinc264/Flood-prediction-Model.git
cd Flood-prediction-Model
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🚀 Running the Project

## ▶️ Start FastAPI Backend

```bash
uvicorn api:app --reload --port 8000
```

### API Documentation

```text
http://localhost:8000/docs
```

---

## ▶️ Start Streamlit Dashboard

Open a new terminal and run:

```bash
streamlit run app.py
```

### Dashboard URL

```text
http://localhost:8501
```

---

# 🔌 API Reference

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API Information |
| GET | `/health` | Health Check |
| GET | `/features` | Feature List |
| POST | `/predict` | Flood Risk Prediction |

---

## 📥 Sample Prediction Request

```bash
curl -X POST http://localhost:8000/predict \
-H "Content-Type: application/json" \
-d '{
  "annual_precipitation": 1500,
  "precipitation_of_wettest_month": 400,
  "precipitation_seasonality": 60,
  "drainage_density": 3.5,
  "drainage_texture": 12.0,
  "basin_relief": 800,
  "annual_mean_temperature": 22,
  "temperature_seasonality": 600,
  "curve_number_amcii": 75,
  "ruggedness_number": 0.8,
  "infiltration_number": 6,
  "climate_type": 2,
  "landcover_type": 1,
  "soil_type": 3
}'
```

---

## 📤 Sample Response

```json
{
  "flood_risk_score": 0.8341,
  "risk_percentage": "83.4%",
  "risk_level": "HIGH",
  "color": "red",
  "message": "Immediate attention required. High probability of flood event.",
  "features_used": 13
}
```

---

# 🐳 Docker Support

## Build Docker Image

```bash
docker build -t riskradar .
```

---

## Run Docker Container

```bash
docker run -p 8000:8000 riskradar
```

---

# 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Machine Learning | XGBoost, Scikit-learn |
| Data Processing | Pandas, NumPy |
| Imbalanced Learning | SMOTE |
| Backend API | FastAPI, Uvicorn |
| Frontend Dashboard | Streamlit |
| Visualization | Plotly, Folium, Matplotlib |
| Deployment | Docker |
| Training Environment | Google Colab |

---

# 📈 Future Scope

- [ ] Real-time weather API integration
- [ ] Hugging Face / Render deployment
- [ ] Global-scale flood dataset expansion
- [ ] SMS & Email flood alerts
- [ ] Mobile-responsive frontend
- [ ] Live geospatial monitoring
- [ ] Cloud deployment pipeline

---

# 📜 License

This project is licensed under the **MIT License**.

You are free to:
- Use
- Modify
- Distribute
- Improve

with proper attribution.

---

# 👨‍💻 Author

## Nitin Chauhan

🎓 B.Tech — AI & Data Science  
🏫 Dr. D.Y. Patil School of Science and Technology

---
# ⭐ If you found this project useful, don't forget to star the repository!
