"""
Centralized logger

Usage:
    from src.logger import get_logger
    log = get_logger(__name__)
    log.info("...")
"""

from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from src.config import cfg

_INITIALIZED: bool = False


def _build_formatter() -> logging.Formatter:
    fmt = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"
    return logging.Formatter(fmt=fmt, datefmt=datefmt)


def setup_logging(
    level: str = "INFO",
    log_to_file: bool = True,
    log_dir: Path | str | None = None,
    log_filename: str = "run.log",
) -> None:
    """
    Configures the root logger once
    Subsequent calls are no-ops
    """
    global _INITIALIZED
    if _INITIALIZED:
        return

    numeric_level = getattr(logging, level.upper(), logging.INFO)
    formatter = _build_formatter()

    root = logging.getLogger()
    root.setLevel(numeric_level)

    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(numeric_level)
    console.setFormatter(formatter)
    root.addHandler(console)

    # File handler (optional)
    if log_to_file and log_dir is not None:
        log_path = Path(log_dir) / log_filename
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=5,
            encoding="utf-8",
        )
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        root.addHandler(file_handler)

    # Suppress third-party loggers
    for noisy in ("matplotlib", "PIL", "urllib3", "numba"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    _INITIALIZED = True


def get_logger(name: str) -> logging.Logger:
    """
    Returns a named logger
    """
    if not _INITIALIZED:
        setup_logging(level=cfg.logging.level,
                      log_to_file=cfg.logging.log_to_file,
                      log_dir=cfg.logging.log_dir,
                      log_filename=cfg.logging.log_filename)
    return logging.getLogger(name)
