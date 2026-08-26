@echo off

cd ..
cd ..

for %%I in (.) do set ProjectName=%%~nxI

echo =====================================
echo Executing in %$ProjectName%
echo =====================================

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
	output
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

set "PROJECT_root_folder=%PROJECT_root_folder:\=/%"
echo project:> config\paths.yaml
echo   root_folder: "%PROJECT_root_folder%">> config\paths.yaml
echo. >> config\paths.yaml
echo data:>> config\paths.yaml
echo   root_folder: data>> config\paths.yaml
echo   raw: raw>> config\paths.yaml
echo   processed: processed>> config\paths.yaml
echo. >> config\paths.yaml
echo models:>> config\paths.yaml
echo   root_folder: models>> config\paths.yaml
echo. >> config\paths.yaml
echo reports:>> config\paths.yaml
echo   root_folder: reports>> config\paths.yaml
echo   search: search>> config\paths.yaml
echo   training: training>> config\paths.yaml

echo =====================================
echo Environment is ready!
echo =====================================
