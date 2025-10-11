"""
pytest configuration file
Configure pytest to properly find modules in the current directory
"""

import sys
import os

# Add the src directory and subdirectories to Python path
src_dir = os.path.dirname(os.path.abspath(__file__))
core_dir = os.path.join(src_dir, 'core')
tests_dir = os.path.join(src_dir, 'tests')

for directory in [src_dir, core_dir, tests_dir]:
    if directory not in sys.path:
        sys.path.insert(0, directory)
