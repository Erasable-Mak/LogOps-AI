from sklearn.ensemble import IsolationForest
import numpy as np

class IFServiceModel:
    def __init__(self, **kw):
        self.model = IsolationForest(n_estimators=200, contamination='auto', random_state=42, **kw)

    def fit(self, X):
        self.model.fit(X)
        return self

    def score(self, X):
        s = -self.model.score_samples(X)  # higher = more anomalous
        s = (s - s.mean()) / (s.std() + 1e-6)
        return s
