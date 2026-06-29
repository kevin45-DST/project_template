@echo off

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
echo Installing dependencies...
echo =====================================

pip install -r requirements.txt

echo Done.

echo =====================================
echo Environment is ready!
echo =====================================
