"""
AROH Configuration - Centralized settings for the Autonomous Risk Management Hub.
Version: 1.0 - Causal Horizon
"""
import os
from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum

class RiskLevel(Enum):
    """Standardized risk levels for consistent assessment."""
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    NEGLIGIBLE = 1

@dataclass
class FirebaseConfig:
    """Firebase configuration for real-time state management."""
    credential_path: str = os.getenv("FIREBASE_CREDENTIALS", "firebase_credentials.json")
    project_id: str = os.getenv("FIREBASE_PROJECT_ID", "aroh-causal-horizon")
    
    # Collections structure
    collections: Dict[str, str] = None
    
    def __post_init__(self):
        if self.collections is None:
            self.collections = {
                "knowledge_graph": "knowledge_graph",
                "risk_nodes": "risk_nodes",
                "mitigation_actions": "mitigation_actions",
                "system_logs": "system_logs",
                "portfolio_state": "portfolio_state"
            }

@dataclass
class GraphConfig:
    """Knowledge graph configuration parameters."""
    max_nodes: int = 10000
    max_edges_per_node: int = 50
    edge_types: List[str] = None
    
    def __post_init__(self):
        if self.edge_types is None:
            self.edge_types = [
                "ownership",
                "correlation",
                "causation",
                "temporal",
                "sentiment",
                "regulatory",
                "geographic"
            ]

@dataclass
class PropagationConfig:
    """Risk propagation algorithm configuration."""
    propagation_speed: float = 0.8  # 0-1 scale
    decay_factor: float = 0.2
    max_iterations: int = 100
    convergence_threshold: float = 0.001

class AROHConfig:
    """Main configuration singleton."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.firebase = FirebaseConfig()
            cls._instance.graph = GraphConfig()
            cls._instance.propagation = PropagationConfig()
            
            # Performance settings
            cls._instance.update_interval_seconds = 30
            cls._instance.max_retries = 3
            cls._instance.retry_delay = 5
            
            # Risk thresholds
            cls._instance.risk_thresholds = {
                RiskLevel.CRITICAL: 0.9,
                RiskLevel.HIGH: 0.7,
                RiskLevel.MEDIUM: 0.5,
                RiskLevel.LOW: 0.3
            }
            
        return cls._instance
    
    def validate(self) -> bool:
        """Validate all configuration parameters."""
        try:
            assert 0 <= self.propagation.propagation_speed <= 1, "Propagation speed must be 0-1"
            assert self.graph.max_nodes > 0, "Max nodes must be positive"
            assert os.path.exists(self.firebase.credential_path) or os.getenv("FIRESTORE_EMULATOR_HOST"), \
                f"Firebase credentials not found at {self.firebase.credential_path}"
            return True
        except AssertionError as e:
            print(f"Configuration validation failed: {e}")
            return False

# Global configuration instance
config = AROHConfig()