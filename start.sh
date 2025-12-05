#!/bin/sh
# 1. Cloud Run gives us $PORT (e.g., 8080 or 5678)
# 2. n8n needs $N8N_PORT
# 3. We bridge them here before starting n8n
export N8N_PORT=$PORT

# 4. Start n8n
n8n start
