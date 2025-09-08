import os
from bs4 import BeautifulSoup

def remove_breadcrumbs(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.html') and filename != 'template.html':
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'html.parser')
                
                # Find and remove the breadcrumb navigation
                breadcrumb = soup.find('nav', {'aria-label': 'breadcrumb'})
                if breadcrumb:
                    breadcrumb.decompose()
            
            # Save the modified content
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(str(soup))
            print(f"Updated: {filename}")

if __name__ == "__main__":
    departments_dir = os.path.join(os.path.dirname(__file__), 'departments')
    remove_breadcrumbs(departments_dir)
