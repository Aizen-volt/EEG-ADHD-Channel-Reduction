"""
Central configuration
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

ROOT_DIR: Path = Path(__file__).resolve().parents[1]
DATA_DIR: Path = ROOT_DIR / "data"
RAW_DATA_DIR: Path = DATA_DIR / "raw"
INTERIM_DATA_DIR: Path = DATA_DIR / "interim"
PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
EXPERIMENTS_DIR: Path = ROOT_DIR / "experiments"
LOGS_DIR: Path = ROOT_DIR / "logs"
CHECKPOINTS_DIR: Path = EXPERIMENTS_DIR / "checkpoints"

# Create directories if they don't exist
for _dir in (RAW_DATA_DIR, PROCESSED_DATA_DIR, LOGS_DIR, CHECKPOINTS_DIR):
    _dir.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# EEG Signal
# ---------------------------------------------------------------------------

@dataclass
class EEGConfig:
    sampling_rate: int = 128    # Hz
    num_channels: int = 19
    epoch_duration: float = 2.0 # seconds
    bandpass_low: float = 0.5   # Hz
    bandpass_high: float = 45.0 # Hz
    notch_freq: float = 50.0    # Hz (EU)


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------

@dataclass
class ModelConfig:
    num_classes: int = 2 # ADHD / control
    dropout: float = 0.5
    learning_rate: float = 1e-3
    weight_decay: float = 1e-4
    batch_size: int = 32
    epochs: int = 100
    early_stopping_patience: int = 10
    seed: int = 42


# ---------------------------------------------------------------------------
# XAI
# ---------------------------------------------------------------------------

@dataclass
class XAIConfig:
    pass


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

@dataclass
class LoggingConfig:
    level: str = "INFO"
    log_to_file: bool = True
    log_dir: Path = LOGS_DIR
    log_filename: str = "run.log"


# ---------------------------------------------------------------------------
# Assembled config
# ---------------------------------------------------------------------------

@dataclass
class Config:
    eeg: EEGConfig = field(default_factory=EEGConfig)
    model: ModelConfig = field(default_factory=ModelConfig)
    xai: XAIConfig = field(default_factory=XAIConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)

    # Convenience shortcuts
    root_dir: Path = ROOT_DIR
    data_dir: Path = DATA_DIR
    raw_data_dir: Path = RAW_DATA_DIR
    interim_data_dir: Path = INTERIM_DATA_DIR
    processed_data_dir: Path = PROCESSED_DATA_DIR
    experiments_dir: Path = EXPERIMENTS_DIR
    logs_dir: Path = LOGS_DIR
    checkpoints_dir: Path = CHECKPOINTS_DIR


# Singleton – import this everywhere
cfg = Config()