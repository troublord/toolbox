#!/usr/bin/env bash
cd "$(dirname "$0")"
read -p "Paste YouTube URL: " URL
../.venv/bin/python summarize.py "$URL"
