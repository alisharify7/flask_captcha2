@echo off
setlocal

:: Define file paths
set base_dir_coverage_result=".\result\coverage"
set base_dir_coverage_result_readme=".\result\coverage\README.md"

set "testing_file_txt=.\result\coverage\text\report.txt"
set "testing_file_txt_dir=.\result\coverage/text"

set "testing_file_md=.\result\coverage\markdown\report.md"
set "testing_file_md_dir=.\result\coverage\markdown"

set "testing_file_html_dir=.\result\coverage\html"

:: Create directory if it doesn't exist
if not exist "%base_dir_coverage_result%" (
    mkdir "%base_dir_coverage_result%"
)
if not exist "%testing_file_txt_dir%" (
    mkdir "%testing_file_txt_dir%"
)
if not exist "%testing_file_md_dir%" (
    mkdir "%testing_file_md_dir%"
)
if not exist "%testing_file_html_dir%" (
    mkdir "%testing_file_html_dir%"
)

:: Delete existing files
del "%testing_file_txt%" >nul 2>&1
del "%testing_file_md%" >nul 2>&1
del "%testing_file_html_dir%\.gitignore"
:: Get date and time
for /f "tokens=2 delims==" %%D in ('wmic Path Win32_LocalTime Get Day /Format:value') do set "day=%%D"
for /f "tokens=2 delims==" %%M in ('wmic Path Win32_LocalTime Get Month /Format:value') do set "month=%%M"
for /f "tokens=2 delims==" %%Y in ('wmic Path Win32_LocalTime Get Year /Format:value') do set "year=%%Y"
for /f "tokens=2 delims==" %%W in ('wmic Path Win32_LocalTime Get DayOfWeek /Format:value') do set "dow=%%W"

for /f "tokens=2 delims==" %%H in ('wmic Path Win32_LocalTime Get Hour /Format:value') do set "HH=%%H"
for /f "tokens=2 delims==" %%N in ('wmic Path Win32_LocalTime Get Minute /Format:value') do set "MM=%%N"
for /f "tokens=2 delims==" %%S in ('wmic Path Win32_LocalTime Get Second /Format:value') do set "SS=%%S"

:: Map day of the week number to name
set "dow_name=Sunday Monday Tuesday Wednesday Thursday Friday Saturday"
for /f "tokens=%dow% delims= " %%D in ("%dow_name%") do set "dow=%%D"

:: Output date and time to the files
(
    echo.
    echo * pytest report
    echo * report date:  %year%/%month%/%day%/ %dow%
    echo * report time:  %HH%:%MM%:%SS%
    echo * operation: coverage result
    echo * author: github.com/alisharify7
    echo * Copyleft 2024. flask-captcha2.
    echo * https://github.com/alisharify7/flask_captcha2
    echo.
) > "%testing_file_txt%"

(
    echo.
    echo * pytest report
    echo * report date:  %year%/%month%/%day%/ %dow%
    echo * report time:  %HH%:%MM%:%SS%
    echo * operation: coverage result
    echo * author: github.com/alisharify7
    echo * Copyleft 2024. flask-captcha2.
    echo * https://github.com/alisharify7/flask_captcha2
    echo.
) > "%base_dir_coverage_result_readme%"

(
    echo.
    echo * pytest report
    echo * report date:  %year%/%month%/%day%/ %dow%
    echo * report time:  %HH%:%MM%:%SS%
    echo * operation: coverage result
    echo * author: github.com/alisharify7
    echo * Copyleft 2024. flask-captcha2.
    echo * https://github.com/alisharify7/flask_captcha2
    echo.
) > "%testing_file_md%"


:: Run pytest and append the results to the files
coverage run -m pytest

:: Redirect coverage report output to both files
(
    coverage report --show --sort miss --precision=3
) >> "%testing_file_txt%"

coverage report --show --sort miss --precision=3 --format=markdown >> "%testing_file_md%"

echo. >> "%testing_file_txt%"
echo. >> "%testing_file_md%"

coverage html -d %testing_file_html_dir%
endlocal