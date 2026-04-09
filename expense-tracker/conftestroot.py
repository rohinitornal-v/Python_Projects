"""
conftestroot.py - pytest configuration file - Root Project Configuration
Adds project root to Python path so imports work correctly
This file is loaded by BOTH pytest AND behave automatically.
Do NOT put test fixtures here - they belong in tests/conftest.py
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
