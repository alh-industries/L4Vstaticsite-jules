import os
import csv

def combine_reports():
    """
    Combines individual SEO CSV reports from the SEO/ directory into a single file.
    """
    seo_dir = 'SEO'
    output_file = os.path.join(seo_dir, 'combined_seo_report.csv')

    # Find all individual report CSVs, excluding the combined one if it exists
    individual_reports = [f for f in os.listdir(seo_dir) if f.endswith('_seo.csv') and f != 'combined_seo_report.csv']

    combined_data = []

    for report_file in individual_reports:
        # Derive the version name from the filename
        version_name = report_file.replace('_seo.csv', '')
        report_path = os.path.join(seo_dir, report_file)

        try:
            with open(report_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Add the version to the row
                    new_row = {'Version': version_name, 'SEO_Element': row['SEO_Element'], 'Value': row['Value']}
                    combined_data.append(new_row)
        except Exception as e:
            print(f"Could not process file {report_path}: {e}")

    if not combined_data:
        print("No data to combine.")
        return

    # Define the fieldnames for the combined CSV
    fieldnames = ['Version', 'SEO_Element', 'Value']

    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(combined_data)
        print(f"Combined report saved to {output_file}")
    except Exception as e:
        print(f"Error writing to {output_file}: {e}")

if __name__ == '__main__':
    combine_reports()
