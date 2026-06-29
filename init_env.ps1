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
Write-Host Installing dependencies...
Write-Host =====================================

pip install -r requirements.txt

Write-Host Done.

Write-Host =====================================
Write-Host Environment is ready!
Write-Host =====================================
