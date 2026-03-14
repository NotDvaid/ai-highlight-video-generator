import numpy as np
from sklearn.ensemble import RandomForestClassifier
<<<<<<< HEAD
import joblib

# Training data
# Features: motion, brightness, sharpness, contrast
X = np.array([
    [0.1, 0.2, 0.1, 0.1],
    [0.9, 0.8, 0.7, 0.8],
    [0.8, 0.7, 0.6, 0.7],
    [0.2, 0.1, 0.2, 0.1],
    [0.7, 0.9, 0.8, 0.6],
    [0.3, 0.2, 0.1, 0.2]
])

# Labels: 1 = highlight, 0 = not highlight
y = np.array([0, 1, 1, 0, 1, 0])

model = RandomForestClassifier()
model.fit(X, y)

joblib.dump(model, "highlight_model.pkl")

=======
from sklearn.model_selection import cross_val_score
import joblib

# Expanded training data
# Features: [motion, brightness, colorfulness, sharpness]
X = np.array([
    # highlight-worthy segments (label=1)
    [0.85, 0.70, 0.75, 0.80],
    [0.90, 0.65, 0.80, 0.85],
    [0.75, 0.80, 0.70, 0.90],
    [0.80, 0.75, 0.85, 0.75],
    [0.70, 0.85, 0.65, 0.80],
    [0.95, 0.60, 0.90, 0.70],
    [0.65, 0.90, 0.80, 0.85],
    [0.88, 0.72, 0.78, 0.82],
    [0.78, 0.68, 0.82, 0.88],
    [0.82, 0.78, 0.72, 0.76],
    # NOT highlight-worthy (label=0)
    [0.10, 0.20, 0.15, 0.10],
    [0.15, 0.15, 0.10, 0.20],
    [0.05, 0.30, 0.20, 0.15],
    [0.20, 0.10, 0.05, 0.25],
    [0.12, 0.25, 0.18, 0.08],
    [0.08, 0.35, 0.12, 0.30],
    [0.25, 0.18, 0.22, 0.12],
    [0.18, 0.22, 0.08, 0.18],
    [0.30, 0.12, 0.15, 0.22],
    [0.22, 0.28, 0.25, 0.15],
    # Edge cases
    [0.50, 0.50, 0.50, 0.50],
    [0.45, 0.55, 0.40, 0.60],
    [0.55, 0.45, 0.55, 0.45],
    [0.40, 0.60, 0.35, 0.55],
])

y = np.array([
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 1, 0,
])

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

scores = cross_val_score(model, X, y, cv=3)
print(f"Cross-validation accuracy: {scores.mean():.2f} (+/- {scores.std():.2f})")

joblib.dump(model, "highlight_model.pkl")
>>>>>>> main
print("Model trained and saved!")