$ProjectName = Split-Path -Leaf $PWD

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

python -m ipykernel install --user `
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
    "tests"
)

foreach ($folder in $folders) {
    New-Item -ItemType Directory -Force -Path $folder | Out-Null
}

Write-Host Done.

Write-Host =====================================
Write-Host Environment is ready!
Write-Host =====================================
