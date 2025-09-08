import os
import re
from bs4 import BeautifulSoup
import shutil

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

def ensure_css_files_exist():
    """Ensure all required CSS files exist in the css directory"""
    css_files = [
        'style.css',
        'header.css',
        'welcome.css',
        'news.css',
        'carousel-styles.css',
        'general.css',
        'footer.css',
        'downloads.css',
        'leadership.css'
    ]
    
    # Create css directory if it doesn't exist
    os.makedirs('css', exist_ok=True)
    
    # Copy CSS files from root to css directory if they don't exist
    for css_file in css_files:
        if os.path.exists(css_file) and not os.path.exists(f'css/{css_file}'):
            shutil.copy2(css_file, f'css/{css_file}')

def fix_relative_paths(html_content, file_depth=1):
    """Fix relative paths in HTML content based on file depth"""
    # Calculate the correct number of '../' to go back to root
    prefix = '../' * file_depth if file_depth > 0 else './'
    
    # Fix CSS and JS paths
    html_content = re.sub(
        r'(<link[^>]*href=["\'])(?!https?://|/|#)([^"\']+["\'])',
        fr'\1{prefix}\2',
        html_content
    )
    html_content = re.sub(
        r'(<script[^>]*src=["\'])(?!https?://|/|#)([^"\']+["\'])',
        fr'\1{prefix}\2',
        html_content
    )
    
    # Fix image paths
    html_content = re.sub(
        r'(<img[^>]*src=["\'])(?!https?://|/|#)([^"\']+["\'])',
        fr'\1{prefix}\2',
        html_content
    )
    
    # Fix anchor hrefs
    html_content = re.sub(
        r'(<a[^>]*href=["\'])(?!https?://|/|#)([^"\']+["\'])',
        fr'\1{prefix}\2',
        html_content
    )
    
    return html_content

def update_page_content(file_path, header, footer):
    """Update a page with the standard header and footer"""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Parse the content with BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')
    
    # Remove existing header
    for tag in soup.find_all(['header', 'nav']) + soup.find_all('div', class_=lambda x: x and 'navbar' in x):
        tag.decompose()
    
    # Remove existing footer
    for footer_tag in soup.find_all('footer'):
        footer_tag.decompose()
    
    # Insert new header at the beginning of body
    if header:
        body = soup.find('body')
        if body:
            body.insert(0, BeautifulSoup(header, 'html.parser'))
    
    # Insert new footer at the end of body
    if footer:
        body = soup.find('body')
        if body:
            body.append(BeautifulSoup(footer, 'html.parser'))
    
    # Get the relative depth of the file
    rel_path = os.path.relpath(file_path, os.path.dirname(os.path.abspath(__file__)))
    file_depth = len(rel_path.split(os.sep)) - 1
    
    # Fix relative paths
    content = str(soup)
    content = fix_relative_paths(content, file_depth)
    
    # Write the updated content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def process_html_file(file_path, header, footer):
    """Process a single HTML file to update header and footer"""
    try:
        # Skip index.html and template files
        filename = os.path.basename(file_path)
        if filename in ['index.html', 'template.html']:
            return False
            
        print(f"Updating {filename}...")
        update_page_content(file_path, header, footer)
        print(f"Successfully updated {filename}")
        return True
    except Exception as e:
        print(f"Error updating {filename}: {str(e)}")
        return False

def main():
    # Ensure CSS files are in the right place
    ensure_css_files_exist()
    
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
        # Skip certain directories
        skip_dirs = ['node_modules', '.git', 'css', 'images', 'js', 'downloadables']
        if any(skip_dir in root for skip_dir in skip_dirs):
            continue
            
        for filename in files:
            if filename.endswith('.html'):
                file_path = os.path.join(root, filename)
                
                # Skip index.html as it's our source
                if filename == 'index.html':
                    continue
                    
                if process_html_file(file_path, header, footer):
                    updated_count += 1
    
    print(f"\nSuccessfully updated {updated_count} HTML files with the standard header and footer.")
    print("Please verify the changes and commit them to the repository.")

if __name__ == "__main__":
    main()
