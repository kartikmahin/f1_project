# 🏎️ F1 Bahrain Grand Prix 2026 Predictor

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-EE4C2C.svg)](https://pytorch.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B.svg)](https://streamlit.io/)

A state-of-the-art Formula 1 race result prediction engine leveraging **Neural Network Ensembles** and **Uncertainty Estimation**. This project specifically targets the upcoming 2026 Bahrain Grand Prix, using historical data and comprehensive driver performance metrics to forecast the finish order.

## ✨ Features

-   **Ensemble Modeling**: Uses multiple neural networks to provide robust predictions and calculate confidence intervals.
-   **Intelligent Feature Engineering**: Analyzes career stats, recent form, grid-to-finish deltas, and track-specific performance (Bahrain focus).
-   **Interactive Dashboard**: A sleek Streamlit-powered UI to visualize predictions, podium probabilities, and driver profiles.
-   **Synthetic Data Generation**: Realistic data simulation for training when live API data is limited.
-   **Uncertainty Estimation**: Predicts not just the position, but the confidence and potential variance (error bars) for each driver.

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

## 🏆 Sample Predictions (Bahrain 2026)

| Position | Driver | Team | Confidence |
| :--- | :--- | :--- | :--- |
| 🥇 1st | Max Verstappen | Red Bull Racing | 92% |
| 🥈 2nd | Lando Norris | McLaren | 88% |
| 🥉 3rd | Charles Leclerc | Ferrari | 85% |

---

*Disclaimer: This project is for educational and entertainment purposes. F1 is unpredictable, and these predictions are based on historical trends and statistical modeling.*
