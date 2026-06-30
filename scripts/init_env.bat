@echo off

for %%I in (.) do set ProjectName=%%~nxI

echo =====================================
echo Creating virtual environment...
echo =====================================

py -m venv env

echo Done.

echo =====================================
echo Activating virtual environment...
echo =====================================

call env\Scripts\activate.bat

echo Done.

echo =====================================
echo Upgrading pip...
echo =====================================

python -m pip install --upgrade pip

echo Done.

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

echo =====================================
echo Installing dependencies...
echo =====================================

pip install -r requirements.txt

echo Done.

echo =====================================
echo Creating project folders...
echo =====================================

for %%D in (
    data\raw
    data\interim
    data\processed
    logs
    models
	output
    src
    tests
    notebooks
) do (
    if not exist "%%D" (
        mkdir "%%D"
        echo Created %%D
    ) else (
        echo Already exists %%D
    )
)

echo =====================================
echo Environment is ready!
echo =====================================
