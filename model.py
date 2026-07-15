"""PyTorch neural network model for F1 position prediction."""
# pyrefly: ignore [missing-import]
import torch
import torch.nn as nn
import numpy as np
import os
from config import MODEL_DIR, FEATURE_COLUMNS

INPUT_DIM = len(FEATURE_COLUMNS)


class F1PredictorNet(nn.Module):
    """Multi-layer neural network for predicting F1 race finish positions."""

    def __init__(self, input_dim=INPUT_DIM, hidden_dims=None):
        super().__init__()
        if hidden_dims is None:
            hidden_dims = [64, 128, 64]

        layers = []
        prev_dim = input_dim
        for h_dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, h_dim),
                nn.BatchNorm1d(h_dim),
                nn.ReLU(),
                nn.Dropout(0.2),
            ])
            prev_dim = h_dim

        # Output: single position prediction
        layers.append(nn.Linear(prev_dim, 1))
        self.network = nn.Sequential(*layers)

    def forward(self, x):
        return self.network(x).squeeze(-1)


class F1EnsembleModel:
    """Ensemble of neural networks for more robust predictions with uncertainty estimation."""

    def __init__(self, n_models=5, input_dim=INPUT_DIM):
        self.n_models = n_models
        self.input_dim = input_dim
        self.models = [F1PredictorNet(input_dim) for _ in range(n_models)]
        self.scaler_mean = None
        self.scaler_std = None

    def _normalize(self, X, fit=False):
        if fit:
            self.scaler_mean = X.mean(axis=0)
            self.scaler_std = X.std(axis=0) + 1e-8
        return (X - self.scaler_mean) / self.scaler_std

    def train(self, X, y, epochs=300, lr=0.001, verbose=True):
        X_norm = self._normalize(X, fit=True)

        for i, model in enumerate(self.models):
            X_tensor = torch.tensor(X_norm, dtype=torch.float32)
            y_tensor = torch.tensor(y, dtype=torch.float32)

            optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=1e-4)
            scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)
            criterion = nn.SmoothL1Loss()  # Huber loss - robust to outliers

            model.train()
            best_loss = float("inf")
            best_state = None

            for epoch in range(epochs):
                # Add noise for regularization (different per model in ensemble)
                noise = torch.randn_like(X_tensor) * 0.05
                pred = model(X_tensor + noise)
                loss = criterion(pred, y_tensor)

                optimizer.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                optimizer.step()
                scheduler.step()

                if loss.item() < best_loss:
                    best_loss = loss.item()
                    best_state = {k: v.clone() for k, v in model.state_dict().items()}

                if verbose and (epoch + 1) % 100 == 0:
                    print(f"  Model {i+1}/{self.n_models} | Epoch {epoch+1}/{epochs} | Loss: {loss.item():.4f}")

            # Load best weights
            if best_state:
                model.load_state_dict(best_state)

        if verbose:
            print("Training complete!")

    def predict(self, X):
        """Return mean prediction and std (uncertainty) across ensemble."""
        X_norm = self._normalize(X, fit=False)
        X_tensor = torch.tensor(X_norm, dtype=torch.float32)

        predictions = []
        for model in self.models:
            model.eval()
            with torch.no_grad():
                pred = model(X_tensor).numpy()
            predictions.append(pred)

        predictions = np.array(predictions)
        mean_pred = predictions.mean(axis=0)
        std_pred = predictions.std(axis=0)
        return mean_pred, std_pred

    def save(self, path=None):
        if path is None:
            path = os.path.join(MODEL_DIR, "f1_ensemble.pth")
        state = {
            "scaler_mean": self.scaler_mean,
            "scaler_std": self.scaler_std,
            "models": [m.state_dict() for m in self.models],
            "input_dim": self.input_dim,
        }
        torch.save(state, path)
        print(f"Model saved to {path}")

    def load(self, path=None):
        if path is None:
            path = os.path.join(MODEL_DIR, "f1_ensemble.pth")
        state = torch.load(path, weights_only=False)
        self.scaler_mean = state["scaler_mean"]
        self.scaler_std = state["scaler_std"]
        self.input_dim = state["input_dim"]
        self.models = [F1PredictorNet(self.input_dim) for _ in range(self.n_models)]
        for m, sd in zip(self.models, state["models"]):
            m.load_state_dict(sd)
        print(f"Model loaded from {path}")


def train_model(X=None, y=None):
    """Train the ensemble model and save it."""
    if X is None or y is None:
        from data_pipeline import prepare_training_data
        X, y, _ = prepare_training_data()

    model = F1EnsembleModel(n_models=5)
    model.train(X, y, epochs=300, lr=0.001)
    model.save()

    # Quick validation
    mean_pred, std_pred = model.predict(X)
    mae = np.mean(np.abs(mean_pred - y))
    print(f"\nTraining MAE: {mae:.2f} positions")
    return model


if __name__ == "__main__":
    train_model()