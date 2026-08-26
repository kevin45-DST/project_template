Set-Location ..

$ProjectName = Split-Path -Leaf $PWD

Write-Host =====================================
Write-Host Executing "in $ProjectName"
Write-Host =====================================

Write-Host =====================================
Write-Host Creating virtual environment...
Write-Host =====================================

py -m venv env

Write-Host Done.

Write-Host =====================================
Write-Host Activating virtual environment...
Write-Host =====================================

.\env\Scripts\activate.ps1

Write-Host Done.

Write-Host =====================================
Write-Host Upgrading pip...
Write-Host =====================================

python -m pip install --upgrade pip

Write-Host Done.

Write-Host =====================================
Write-Host Installing ipykernel...
Write-Host =====================================

pip install ipykernel

Write-Host Done.

Write-Host =====================================
Write-Host Creating Jupyter kernel...
Write-Host =====================================

python -m ipykernel install `
    --sys-prefix `
    --name $ProjectName `
    --display-name "Python ($ProjectName)"

Write-Host Done.

Write-Host =====================================
Write-Host Installing dependencies...
Write-Host =====================================

pip install -r requirements.txt

Write-Host Done.

Write-Host =====================================
Write-Host Creating project folders...
Write-Host =====================================

$folders = @(
    "data/raw",
    "data/processed",
    "logs",
    "models",
	"outputs",
    "notebooks",
    "src",
    "tests",
    "config"
)

foreach ($folder in $folders) {
    New-Item -ItemType Directory -Force -Path $folder | Out-Null
}

Write-Host Done.

Write-Host =====================================
Write-Host initialisation paths.yaml...
Write-Host =====================================

$Projectroot_folder = (Get-Location).Path -replace "\\", "/"

@"
project:
  root_folder: "$projectroot_folder"

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
"@ | Set-Content "config/paths.yaml"

Write-Host =====================================
Write-Host Environment is ready!
Write-Host =====================================
