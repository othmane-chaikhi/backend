@echo off
echo ==================================
echo   Portfolio Backend Server
echo ==================================
echo.

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Check if migrations exist
if not exist "db.sqlite3" (
    echo First time setup - creating database...
    python manage.py migrate
    echo.
    echo Creating admin user...
    python create_admin.py
    echo.
)

:: Start server
echo Starting Django development server...
echo Backend will be available at: http://localhost:8000
echo API Documentation: http://localhost:8000/swagger/
echo.
echo Press CTRL+C to stop the server
echo.
python manage.py runserver

