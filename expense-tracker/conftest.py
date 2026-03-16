"""
conftest.py - pytest configuration file
Adds project root to Python path so imports work correctly
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
