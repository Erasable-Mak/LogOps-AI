import pickle
from pathlib import Path
from typing import Optional, Tuple

class ModelRegistry:
    def __init__(self, models_dir: Path):
        self.models_dir = models_dir
        self.models_dir.mkdir(parents=True, exist_ok=True)
    
    def save_iforest(self, service: str, model, featurizer):
        """Save Isolation Forest model and featurizer for a service"""
        service_dir = self.models_dir / service
        service_dir.mkdir(exist_ok=True)
        
        with open(service_dir / "model.pkl", "wb") as f:
            pickle.dump(model, f)
        with open(service_dir / "featurizer.pkl", "wb") as f:
            pickle.dump(featurizer, f)
    
    def load_iforest(self, service: str):
        """Load Isolation Forest model and featurizer for a service"""
        service_dir = self.models_dir / service
        model_path = service_dir / "model.pkl"
        featurizer_path = service_dir / "featurizer.pkl"
        
        if not model_path.exists() or not featurizer_path.exists():
            return None
            
        try:
            with open(model_path, "rb") as f:
                model = pickle.load(f)
            with open(featurizer_path, "rb") as f:
                featurizer = pickle.load(f)
            return model, featurizer
        except:
            return None
