#!/usr/bin/env python3
"""
Entry point for the Panch-Angam Flask application.
This file redirects to the main application in fresh_panchangam_webapp/app.py
"""

import sys
import os

# Add the fresh_panchangam_webapp directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'fresh_panchangam_webapp'))

# Import the main Flask app
from fresh_panchangam_webapp.app import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 