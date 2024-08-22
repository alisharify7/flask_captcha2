#!/bin/bash

# Define file paths (modify these if needed)
base_dir_pytest_result="./result/pytest"
base_dir_pytest_result_readme="./result/pytest/README.md"
testing_file_txt="./result/pytest/text/report.txt"
testing_file_txt_dir="./result/pytest/text"
testing_file_html_dir="./result/pytest/html"

# Create directories if they don't exist
mkdir -p "$base_dir_pytest_result" "$testing_file_txt_dir"

# Get date
date_str=$(date +%d/%m/%Y/%A)

# Get time
time_str=$(date +%H:%M:%S)

# Report header information
report_header="* pytest report
* report date:  $date_str
* report time:  $time_str
* operation: tests result
* author: github.com/alisharify7
* Copyleft 2024. flask-captcha2.
* https://github.com/alisharify7/flask_captcha2"

# Create report headers
echo "$report_header" > "$base_dir_pytest_result_readme"
echo "$report_header" > "$testing_file_txt"

# Run pytest and capture output
pytest -v > "$testing_file_txt" 2>&1

# Generate HTML report with self-contained content
pytest --html="$testing_file_html_dir/report.html" --self-contained-html