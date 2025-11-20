#!/bin/bash

echo "🛡️  DLP Platform - Quick Start"
echo "=============================="
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate and install dependencies
echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "Choose an option:"
echo "  1) Run Streamlit Dashboard (Recommended)"
echo "  2) Run FastAPI Server"
echo "  3) Run Tests"
echo "  4) Run Docker Compose"
echo ""
read -p "Enter choice [1-4]: " choice

case $choice in
    1)
        echo "Starting Streamlit dashboard on http://localhost:8501"
        streamlit run dashboard/app.py
        ;;
    2)
        echo "Starting FastAPI server on http://localhost:8000"
        echo "API Docs available at http://localhost:8000/docs"
        python api/server.py
        ;;
    3)
        echo "Running tests..."
        python -m unittest discover tests -v
        ;;
    4)
        echo "Starting Docker Compose..."
        docker-compose up --build
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac
