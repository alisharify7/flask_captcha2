#!/bin/bash

# Define file paths (modify these if needed)
base_dir_coverage_result="./result/coverage"
base_dir_coverage_result_readme="./result/coverage/README.md"

testing_file_txt="./result/coverage/text/report.txt"
testing_file_txt_dir="./result/coverage/text"

testing_file_md="./result/coverage/markdown/report.md"
testing_file_md_dir="./result/coverage/markdown"

testing_file_html_dir="./result/coverage/html"


# Delete existing files (using redirection for potential errors)
rm -f "$testing_file_txt" "$testing_file_md" "$testing_file_html_dir/.gitignore" 2>/dev/null

# Create directories if they don't exist
mkdir -p "$base_dir_coverage_result" "$testing_file_txt_dir" "$testing_file_md_dir" "$testing_file_html_dir"

# Get date and time
date_str=$(date +%d/%m/%Y/%A)
time_str=$(date +%H:%M:%S)

# Header information for reports
report_header="* pytest report
* report date:  $date_str
* report time:  $time_str
* operation: coverage result
* author: github.com/alisharify7
* Copyleft 2024. flask-captcha2.
* https://github.com/alisharify7/flask_captcha2"

# Create report headers (using redirection for potential errors)
echo "$report_header" > "$testing_file_txt" 2>/dev/null
echo  >> "$testing_file_txt" 2>/dev/null

echo "$report_header" > "$base_dir_coverage_result_readme" 2>/dev/null
echo  >> "$base_dir_coverage_result_readme" 2>/dev/null

echo "$report_header" > "$testing_file_md" 2>/dev/null
echo  >> "$testing_file_md" 2>/dev/null

# Run pytest and append results to text and markdown files
coverage run  --source=../flask_captcha2/ -m pytest .

coverage report --show --sort miss --precision=3 | cut -d '/' -f 8-  >> "$testing_file_txt"
coverage report --show --sort miss --precision=3 --format=markdown >> "$testing_file_md"

echo "" >> "$testing_file_txt"  # Add empty line
echo "" >> "$testing_file_md"    # Add empty line

# Generate HTML report
coverage html -d "$testing_file_html_dir"