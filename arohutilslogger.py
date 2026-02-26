"""
AROH Logging System - Structured logging for monitoring and debugging.
"""
import logging
import sys
from datetime import datetime
from typing import Dict, Any, Optional
import json
from enum import Enum

class LogLevel(Enum):
    """Extended log levels for risk management."""
    TRACE = 5
    DEBUG = 10
    INFO = 20
    RISK = 25  # Custom level for risk events
    WARNING = 30
    MITIGATION = 35  # Custom level for mitigation actions
    ERROR = 40
    CRITICAL = 50

class AROHLogger:
    """Centralized logging system with Firebase integration capability."""
    
    def __init__(self, name: str = "AROH", firebase_client = None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Add custom log levels
        logging.addLevelName(LogLevel.RISK.value, "RISK")
        logging.addLevelName(LogLevel.MITIGATION.value, "MITIGATION")
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Custom formatter with timestamp and module info
        formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(module)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        
        # Remove existing handlers to avoid duplicates
        self.logger.handlers.clear()
        self.logger.addHandler(console_handler)
        
        # Firebase client for remote logging
        self.firebase_client = firebase_client
        
        # Log initialization
        self.info(f"AROH Logger initialized for {name}")
    
    def _log_to_firebase(self, level: str, message: str, extra_data: Dict[str, Any] = None):
        """Send log entry to Firebase if client is available."""
        if self.firebase_client:
            try:
                log_entry = {
                    "timestamp": datetime.utcnow().isoformat(),
                    "level": level,
                    "message": message,
                    "module": self.logger.name,
                    "data