FROM n8nio/n8n:latest

USER root

# Install Python (optional, for your ML logic)
RUN apk add --no-cache python3 py3-pip

# Copy the start script and make it executable
COPY start.sh /start.sh
RUN chmod +x /start.sh

USER node

# We use the script to handle the port mapping safely
ENTRYPOINT ["/start.sh"]
