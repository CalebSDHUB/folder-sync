#!/bin/bash

# Script to run the FolderSync Python program

# Path to the Python script
SCRIPT_PATH="folder_sync.py"

# Parameters
SRC_PATH="src/"
DST_PATH="dst/"
PERIOD=5  # Synchronization interval in seconds
LOG_PATH="sync.log"

# Run the Python script with the specified parameters
# python "$SCRIPT_PATH" --src "$SRC" --dst "$DST" --period "$PERIOD" --log "$LOG"
python "$SCRIPT_PATH" --src "$SRC_PATH" --dst "$DST_PATH" --interval "$PERIOD" --logfile "$LOG_PATH"