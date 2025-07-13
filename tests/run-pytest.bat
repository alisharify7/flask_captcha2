@echo off

:: Define file paths
set base_dir_pytest_result=".\result\pytest"
set base_dir_pytest_result_readme=".\result\pytest\README.md"
set "testing_file_txt=.\result\pytest\text\report.txt"
set "testing_file_txt_dir=.\result\pytest\text\"
set "testing_file_html_dir=.\result\pytest\html"

:: Create directory if it doesn't exist
if not exist "%base_dir_pytest_result%" (
    mkdir "%base_dir_pytest_result%"
)
if not exist "%testing_file_txt_dir%" (
    mkdir "%testing_file_txt_dir%"
)


:: Get date
for /f "tokens=2 delims==" %%D in ('wmic Path Win32_LocalTime Get Day /Format:value') do set "day=%%D"
for /f "tokens=2 delims==" %%M in ('wmic Path Win32_LocalTime Get Month /Format:value') do set "month=%%M"
for /f "tokens=2 delims==" %%Y in ('wmic Path Win32_LocalTime Get Year /Format:value') do set "year=%%Y"
for /f "tokens=2 delims==" %%W in ('wmic Path Win32_LocalTime Get DayOfWeek /Format:value') do set "dow=%%W"

:: Get time
for /f "tokens=2 delims==" %%H in ('wmic Path Win32_LocalTime Get Hour /Format:value') do set "HH=%%H"
for /f "tokens=2 delims==" %%N in ('wmic Path Win32_LocalTime Get Minute /Format:value') do set "MM=%%N"
for /f "tokens=2 delims==" %%S in ('wmic Path Win32_LocalTime Get Second /Format:value') do set "SS=%%S"

:: Map day of the week number to name
set "dow_name=Sunday Monday Tuesday Wednesday Thursday Friday Saturday"
for /f "tokens=%dow% delims= " %%D in ("%dow_name%") do set "dow=%%D"


:: Additional information
:: Ownership notice
(
    echo.
    echo * pytest report
    echo * report date:  %year%/%month%/%day%/ %dow%
    echo * report time:  %HH%:%MM%:%SS%
    echo * operation: tests result
    echo * author: github.com/alisharify7
    echo * Copyleft 2024. flask-captcha2.
    echo * https://github.com/alisharify7/flask_captcha2
    echo.
) > "%base_dir_pytest_result_readme%"
(
    echo.
    echo * pytest report
    echo * report date:  %year%/%month%/%day%/ %dow%
    echo * report time:  %HH%:%MM%:%SS%
    echo * operation: tests result
    echo * author: github.com/alisharify7
    echo * Copyleft 2024. flask-captcha2.
    echo * https://github.com/alisharify7/flask_captcha2
    echo.
) > "%testing_file_txt%"



:: Run pytest and append the result to the file
pytest -v >> %testing_file_txt%
pytest --html="%testing_file_html_dir%\report.html" --self-contained-html
