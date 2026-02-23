@echo off
cd /d C:\Project\data-analytics-portfolio\03-projects\01-ecommerce-price-tracker

echo Running scraper...
venv\Scripts\python.exe -m scripts.daily_scrape

echo.
echo Press any key to exit...
pause