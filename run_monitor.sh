#!/bin/bash
SCRIPT_PATH="Server Monitor.py"

python3 "$SCRIPT_PATH" >> /var/log/server_monitor.log 2>&1