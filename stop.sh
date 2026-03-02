#!/bin/bash

cd "$(dirname "$0")"

source ports.env

lsof -ti:$BACKEND_PORT  | xargs kill 2>/dev/null && echo "Backend (port $BACKEND_PORT) stopped"  || echo "Backend not running"
lsof -ti:$FRONTEND_PORT | xargs kill 2>/dev/null && echo "Frontend (port $FRONTEND_PORT) stopped" || echo "Frontend not running"
