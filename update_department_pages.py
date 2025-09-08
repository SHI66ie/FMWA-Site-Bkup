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

def process_html_file(file_path, header, footer):
    """Process a single HTML file to update header and footer"""
    try:
        # Skip index.html and template files
        if os.path.basename(file_path) in ['index.html', 'template.html']:
            return False
            
        print(f"Updating {os.path.basename(file_path)}...")
        update_department_page(file_path, header, footer)
        print(f"Successfully updated {os.path.basename(file_path)}")
        return True
    except Exception as e:
        print(f"Error updating {os.path.basename(file_path)}: {str(e)}")
        return False

def main():
    # Get the standard header and footer from index.html
    header, footer = get_header_footer()
    if not header or not footer:
        print("Error: Could not find header or footer in index.html")
        return
    
    # Get the project root directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    updated_count = 0
    
    # Process all HTML files in the project
    for root, _, files in os.walk(project_root):
        # Skip certain directories if needed
        if 'node_modules' in root or '.git' in root:
            continue
            
        for filename in files:
            if filename.endswith('.html'):
                file_path = os.path.join(root, filename)
                relative_path = os.path.relpath(file_path, project_root)
                
                # Skip index.html as it's our source
                if filename == 'index.html':
                    continue
                    
                if process_html_file(file_path, header, footer):
                    updated_count += 1
    
    print(f"\nProcessed {updated_count} HTML files with the standard header and footer.")

if __name__ == "__main__":
    main()
