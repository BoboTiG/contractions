#!/bin/bash
set -eu
python -m ruff format server.py
python -m ruff check --fix --unsafe-fixes server.py
python -m mypy server.py
