#!/bin/bash

# Specify the path to your project directory
PROJECT_DIR="/home/pilab/Desktop/babylon/hanginggarden"

# Create a new tmux session for the Django server
tmux new-session -d -s django_server -c "$PROJECT_DIR"

# Send commands to the Django server tmux session
tmux send-keys -t django_server "
source .venv/bin/activate
python manage.py runserver 0.0.0.0:8000" C-m

# Create a new tmux session for the Python script
tmux new-session -d -s python_script -c "$PROJECT_DIR/scheduler"

# Send commands to the Python script tmux session
tmux send-keys -t python_script "
source ../../../.venv/bin/activate
python scheduler.py" C-m
