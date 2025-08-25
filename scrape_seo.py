import os
import csv
import argparse
from bs4 import BeautifulSoup

def scrape_seo_details(html_file_path):
    """
    Scrapes SEO details from a single HTML file.

    Args:
        html_file_path (str): The path to the HTML file.

    Returns:
        list: A list of dictionaries, where each dictionary represents a row in the CSV.
    """
    details = []
    try:
        with open(html_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            soup = BeautifulSoup(f, 'html.parser')

        # File Path
        details.append({'SEO_Element': 'File Path', 'Value': html_file_path})

        # Title
        title = soup.find('title')
        details.append({'SEO_Element': 'Title', 'Value': title.get_text(strip=True) if title else 'Not Found'})

        # Meta tags
        meta_tags = {
            'description': 'Meta Description',
            'keywords': 'Meta Keywords',
            'author': 'Meta Author',
            'viewport': 'Meta Viewport',
            'robots': 'Meta Robots'
        }
        for name, key in meta_tags.items():
            tag = soup.find('meta', attrs={'name': name})
            details.append({'SEO_Element': key, 'Value': tag['content'] if tag else 'Not Found'})

        # Canonical URL
        canonical = soup.find('link', attrs={'rel': 'canonical'})
        details.append({'SEO_Element': 'Canonical URL', 'Value': canonical['href'] if canonical else 'Not Found'})

        # Header tags
        for i in range(1, 7):
            headers = soup.find_all(f'h{i}')
            for j, header in enumerate(headers):
                details.append({'SEO_Element': f'h{i}_{j+1}', 'Value': header.get_text(strip=True)})

        # Image Alt Texts
        images = soup.find_all('img')
        for i, img in enumerate(images):
            alt_text = img.get('alt', 'Not Found')
            details.append({'SEO_Element': f'Image Alt_{i+1}', 'Value': alt_text})

        # Links
        links = soup.find_all('a')
        for i, link in enumerate(links):
            href = link.get('href', 'Not Found')
            details.append({'SEO_Element': f'Link_{i+1}', 'Value': href})

        # Open Graph tags
        og_tags = soup.find_all('meta', property=lambda x: x and x.startswith('og:'))
        for tag in og_tags:
            details.append({'SEO_Element': tag['property'], 'Value': tag['content']})

        # Twitter Card tags
        twitter_tags = soup.find_all('meta', attrs={'name': lambda x: x and x.startswith('twitter:')})
        for tag in twitter_tags:
            details.append({'SEO_Element': tag['name'], 'Value': tag['content']})

        # Language
        lang = soup.html.get('lang') if soup.html else 'Not Found'
        details.append({'SEO_Element': 'Language', 'Value': lang if lang else 'Not Found'})

    except Exception as e:
        details.append({'SEO_Element': 'Error', 'Value': f"Could not process file {html_file_path}: {e}"})

    return details


def main():
    parser = argparse.ArgumentParser(description='Scrape SEO details from HTML files in a directory.')
    parser.add_argument('directory', help='The directory to search for HTML files.')
    parser.add_argument('output_file', help='The path to the output CSV file.')
    args = parser.parse_args()

    all_seo_details = []
    for root, _, files in os.walk(args.directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                all_seo_details.extend(scrape_seo_details(file_path))
                # Add a separator for clarity between files in the CSV
                all_seo_details.append({'SEO_Element': '---', 'Value': '---'})

    if not all_seo_details:
        print("No HTML files found or no data extracted.")
        return

    with open(args.output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['SEO_Element', 'Value'])
        writer.writeheader()
        writer.writerows(all_seo_details)

    print(f"SEO details saved to {args.output_file}")


if __name__ == '__main__':
    main()
