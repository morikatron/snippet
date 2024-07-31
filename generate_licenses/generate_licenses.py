import json
import subprocess


def run_pip_licenses_summary(summay_file):
    # Run pip-licenses command to generate the summary file
    subprocess.run(
        [
            "pip-licenses",
            "--summary",
            f"--output-file={summay_file}",
        ],
        check=True,
    )


def run_pip_licenses(json_file):
    # Run pip-licenses command to generate the JSON file
    subprocess.run(
        [
            "pip-licenses",
            "--format=json",
            "--no-license-path",
            "--with-license-file",
            "--with-urls",
            "--with-authors",
            f"--output-file={json_file}",
        ],
        check=True,
    )


def json_to_plain_text(json_file, output_file):
    with open(json_file, "r", encoding="utf-8") as f:
        licenses = json.load(f)

    with open(output_file, "w", encoding="utf-8") as f:
        for license_info in licenses:
            f.write(f"Name: {license_info['Name']}\n")
            f.write(f"Version: {license_info['Version']}\n")
            f.write(f"License: {license_info['License']}\n")
            f.write(f"Author: {license_info.get('Author', 'N/A')}\n")
            f.write(f"URL: {license_info.get('URL', 'N/A')}\n")
            f.write("License File:\n")
            f.write(f"{license_info['LicenseText']}\n")
            f.write("\n" + "-" * 60 + "\n\n")


if __name__ == "__main__":
    json_file = "licenses.json"
    output_file = "licenses.txt"
    summary_file = "licenses_summary.txt"

    # Run pip-licenses and generate the JSON file
    run_pip_licenses(json_file)

    # Convert JSON to plain text
    json_to_plain_text(json_file, output_file)

    print(f"License information has been written to {output_file}")

    # Run pip-licenses summary and generate the summary file
    run_pip_licenses_summary(summary_file)

    print(f"License summary has been written to {summary_file}")

