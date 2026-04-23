"""
Pytest configuration and shared fixtures
"""
import pytest
import os
import sys
from pathlib import Path

# Add backend directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))
