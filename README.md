# 🏎️ F1 Universal Race Predictor

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-EE4C2C.svg)](https://pytorch.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B.svg)](https://streamlit.io/)

A state-of-the-art Formula 1 race result prediction engine leveraging **Neural Network Ensembles** and **Uncertainty Estimation**. Predict the outcome of **any F1 Grand Prix** — past, present, or future — with intelligent behavior based on whether the race has already happened.

## 🌟 How It Works

| Scenario | What You See |
| :--- | :--- |
| **Past Race** | ✅ Actual race standings **side-by-side** with predictions + accuracy metrics |
| **Future Race** | 🔮 Banner: "This race hasn't happened yet" + predicted positions with confidence |

## ✨ Features

-   **Universal Race Prediction**: Select any GP from 2024–2026 and get predictions instantly.
-   **Past vs Future Intelligence**: Automatically detects if a race has happened and adapts the display.
-   **Ensemble Modeling**: Uses multiple neural networks for robust predictions and confidence intervals.
-   **Accuracy Analysis**: For past races, see MAE, podium accuracy, and position-by-position comparison.
-   **Interactive Dashboard**: A premium Streamlit-powered UI with dark theme, glassmorphism cards, and animated charts.
-   **Driver Deep Dive**: Radar charts and feature profiles for any driver at any GP.

## 🛠️ Tech Stack

-   **Core**: Python
-   **Deep Learning**: PyTorch (Neural Network Architecture)
-   **Data Processing**: Pandas, NumPy, Scikit-learn
-   **F1 Data**: FastF1 API
-   **Frontend**: Streamlit
-   **Visualization**: Plotly

## 🚀 Getting Started

### Prerequisites

-   Python 3.8+
-   `pip` (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/f1_project.git
   cd f1_project
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Dashboard

Launch the interactive predictor:
```bash
streamlit run dashboard.py
```

### CLI Prediction

Predict any race from the command line:
```bash
python race_predictor.py 2024 "Bahrain Grand Prix"
python race_predictor.py 2026 "Monaco Grand Prix"
```

### Data Pipeline

To collect fresh data or generate features:
```bash
python data_pipeline.py
```

## 📊 Model Architecture

The prediction engine is an ensemble of Feed-Forward Neural Networks. Each model in the ensemble is trained on a different subset of data or initialized differently to capture diverse patterns. 

**Key Metrics Analyzed:**
-   **Average Position**: Historical finishing average.
-   **Form (Recent ROI)**: Performance over the last 5 races.
-   **Consistency**: Position volatility and standard deviation.
-   **Trend**: Improvement/Decline trajectories.
-   **Overtaking Delta**: Difference between starting grid and final finish position.
-   **Track-Specific Performance**: How the driver performs at the selected circuit.

## 🏆 Example: Past Race (2024 Bahrain GP)

Shows actual results alongside predictions with accuracy metrics:

| # | Driver | Actual Pos | Predicted Pos | Delta |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Max Verstappen | 1 | 1.2 | +0.2 |
| 2 | Sergio Perez | 2 | 3.5 | +1.5 |
| 3 | Carlos Sainz | 3 | 2.8 | -0.2 |

## 🔮 Example: Future Race (2026 Monaco GP)

Shows predictions only with a banner:

> ⚠️ This race hasn't happened yet — showing predicted positions only.

| # | Driver | Team | Predicted Pos | Confidence |
| :--- | :--- | :--- | :--- | :--- |
| 🥇 1st | Max Verstappen | Red Bull Racing | 1.3 | 92% |
| 🥈 2nd | Lando Norris | McLaren | 2.1 | 88% |
| 🥉 3rd | Charles Leclerc | Ferrari | 2.8 | 85% |

---

*Disclaimer: This project is for educational and entertainment purposes. F1 is unpredictable, and these predictions are based on historical trends and statistical modeling.*
