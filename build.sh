#!/usr/bin/env bash
# exit on error
set -o errexit

# Store Playwright browsers in a location Render can cache them
export PLAYWRIGHT_BROWSERS_PATH=/opt/render/.cache/ms-playwright

pip install -r requirements.txt
playwright install chromium
