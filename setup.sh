#!/bin/bash

# Create .streamlit directory if it doesn't exist
mkdir -p .streamlit

# Create credentials.toml file
cat << EOF > .streamlit/credentials.toml
[general]
email = "user@example.com"
EOF

# Create config.toml file
cat << EOF > .streamlit/config.toml
[server]
headless = true
enableCORS = false
enableXsrfProtection = false
port = $PORT
EOF

echo "✅ Render setup completed successfully!"