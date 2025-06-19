#!/bin/bash

# Setup Cron + Docker

echo "Setting up Cricket ML App"

# Build and run Docker
sudo docker compose up -d
/usr/bin/docker exec cricket_predictor python3 scripts/fetch_cricsheet.py
/usr/bin/docker exec cricket_predictor python3 scripts/parse_yaml_to_csv.py
/usr/bin/docker exec cricket_predictor python3 scripts/train_model.py

# Setup cron job on host

CRON_JOB="0 3 * * * /usr/bin/docker exec cricket_predictor python3 scripts/fetch_cricsheet.py"
(crontab -l | grep -v -F "$CRON_JOB"; echo "$CRON_JOB") | crontab -
/usr/bin/docker exec cricket_predictor python3 scripts/fetch_cricsheet.py
CRON_JOB="0 3 * * * /usr/bin/docker exec cricket_predictor python3 scripts/parse_yaml_to_csv.py"
(crontab -l | grep -v -F "$CRON_JOB"; echo "$CRON_JOB") | crontab -
CRON_JOB="0 3 * * * /usr/bin/docker exec cricket_predictor python3 scripts/train_model.py"
(crontab -l | grep -v -F "$CRON_JOB"; echo "$CRON_JOB") | crontab -

echo "✅ Cron job installed to run daily at 3 AM"
