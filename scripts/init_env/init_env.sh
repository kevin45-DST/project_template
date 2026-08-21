#!/bin/bash
cd ..
cd ..

ProjectName=$(basename "$PWD")

echo "====================================="
echo "Executing in $ProjectName"
echo "====================================="

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

python -m ipykernel install `
    --sys-prefix `
    --name $ProjectName `
    --display-name "Python ($ProjectName)"

echo Done.

echo ""
echo "====================================="
echo "Installing dependencies..."
echo "====================================="

pip install -r requirements.txt

echo "Done."

echo =====================================
echo Creating project folders...
echo =====================================

for %%D in (
    data\raw
    data\interim
    data\processed
    src
    tests
    notebooks
    config
) do (
    if not exist "%%D" (
        mkdir "%%D"
        echo Created %%D
    ) else (
        echo Already exists %%D
    )
)


echo =====================================
echo initialisation paths.yaml...
echo =====================================

PROJECT_root_folder="$(pwd)"

cat > config/paths.yaml <<EOF
project:
  root_folder: "$PROJECT_root_folder"

data:
  root_folder: data 
  raw: raw
  processed: processed

models:
  root_folder: models

reports:
  root_folder: reports
  search: search
  training: training
EOF

echo ""
echo "====================================="
echo "Environment is ready!"
echo "====================================="
```
