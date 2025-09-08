import os
import re
from bs4 import BeautifulSoup

def get_header_footer():
    """Extract header and footer from index.html"""
    with open('index.html', 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        
        # Get header (from start of body to before main content)
        header = soup.find('body').find('header')
        if not header:
            header = soup.find('nav') or soup.find('div', class_='navbar')
        
        # Get footer
        footer = soup.find('footer')
        
        return str(header) if header else '', str(footer) if footer else ''

def update_department_page(file_path, header, footer):
    """Update a department page with the standard header and footer"""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')
    
    # Update header if it exists
    existing_header = soup.find('header') or soup.find('nav') or soup.find('div', class_='navbar')
    if existing_header and header:
        existing_header.replace_with(BeautifulSoup(header, 'html.parser'))
    
    # Update footer if it exists
    existing_footer = soup.find('footer')
    if existing_footer and footer:
        existing_footer.replace_with(BeautifulSoup(footer, 'html.parser'))
    
    # Update CSS and JS paths
    content = str(soup)
    content = re.sub(
        r'(<link[^>]*href=["\'])(?!https?://|/|#)([^"\']+["\'])',
        r'\1../\2',
        content
    )
    content = re.sub(
        r'(<script[^>]*src=["\'])(?!https?://|/|#)([^"\']+["\'])',
        r'\1../\2',
        content
    )
    
    # Write the updated content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def main():
    # Get the standard header and footer from index.html
    header, footer = get_header_footer()
    if not header or not footer:
        print("Warning: Could not find header or footer in index.html")
    
    # Update all department pages
    departments_dir = os.path.join(os.path.dirname(__file__), 'departments')
    
    for filename in os.listdir(departments_dir):
        if filename.endswith('.html') and filename != 'template.html':
            file_path = os.path.join(departments_dir, filename)
            print(f"Updating {filename}...")
            try:
                update_department_page(file_path, header, footer)
                print(f"Successfully updated {filename}")
            except Exception as e:
                print(f"Error updating {filename}: {str(e)}")
    
    print("\nAll department pages have been processed!")

if __name__ == "__main__":
    main()
