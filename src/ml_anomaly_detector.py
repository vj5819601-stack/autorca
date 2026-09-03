from dataclasses import dataclass
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.feature_extraction.text import TfidfVectorizer

@dataclass
class AnomalyResult:
    score: float
    is_anomaly: bool
    top_terms: list

class LogAnomalyDetector:
    """TF-IDF + Isolation Forest detector for unusual log messages."""

    def __init__(self, contamination=0.15, random_state=42):
        self.vectorizer = TfidfVectorizer(
            lowercase=True, ngram_range=(1, 2), min_df=1, max_features=1500
        )
        self.model = IsolationForest(
            contamination=contamination, random_state=random_state, n_estimators=200
        )
        self._fitted = False
        self._matrix = None

    def fit(self, messages):
        self._matrix = self.vectorizer.fit_transform(messages)
        self.model.fit(self._matrix)
        self._fitted = True
        return self

    def score_messages(self, messages):
        if not self._fitted:
            self.fit(messages)
        matrix = self.vectorizer.transform(messages)
        raw = self.model.decision_function(matrix)
        # Higher is more anomalous: normalize inverted decision function.
        anomaly = 1.0 - (raw - raw.min()) / (raw.max() - raw.min() + 1e-9)
        labels = self.model.predict(matrix)
        results = []
        names = np.array(self.vectorizer.get_feature_names_out())
        for i, row in enumerate(matrix):
            weights = row.toarray().ravel()
            top = names[np.argsort(weights)[-5:][::-1]].tolist()
            results.append(AnomalyResult(
                score=float(anomaly[i]),
                is_anomaly=bool(labels[i] == -1),
                top_terms=top,
            ))
        return results
