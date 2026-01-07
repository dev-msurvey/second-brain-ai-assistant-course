"""
Test Configuration
==================

pytest configuration for Module 7 tests.
"""

import pytest
import os
from pathlib import Path


def pytest_configure(config):
    """Configure pytest."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment."""
    # Create test directories
    Path("test_output").mkdir(exist_ok=True)
    Path("test_temp").mkdir(exist_ok=True)
    
    yield
    
    # Cleanup (optional)
    # shutil.rmtree("test_output", ignore_errors=True)
    # shutil.rmtree("test_temp", ignore_errors=True)
