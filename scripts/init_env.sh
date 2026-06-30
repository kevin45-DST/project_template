#!/bin/bash

ProjectName=$(basename "$PWD")

echo "====================================="
echo "Creating virtual environment..."
echo "====================================="

python -m venv env

echo "Done."

echo ""
echo "====================================="
echo "Activating virtual environment..."
echo "====================================="

source env/bin/activate

echo "Done."

echo ""
echo "====================================="
echo "Upgrading pip..."
echo "====================================="

python -m pip install --upgrade pip

echo "Done."

echo =====================================
echo Installing ipykernel...
echo =====================================

pip install ipykernel

echo Done.

echo =====================================
echo Creating Jupyter kernel...
echo =====================================

python -m ipykernel install --user `
    --name $ProjectName `
    --display-name "Python ($ProjectName)"

echo Done.

echo ""
echo "====================================="
echo "Installing dependencies..."
echo "====================================="

pip install -r requirements.txt

echo "Done."

echo ""
echo "====================================="
echo "Environment is ready!"
echo "====================================="
```
