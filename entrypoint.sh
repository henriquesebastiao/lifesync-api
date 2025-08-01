#!/bin/sh

alembic upgrade head
fastapi run lifesync/main.py --host 0.0.0.0 --port 8000 --workers 4