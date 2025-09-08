import os
from bs4 import BeautifulSoup

def remove_header_panel(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.html') and filename != 'template.html':
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'html.parser')
                
                # Remove the header panel
                header = soup.find('header', class_='department-header')
                if header:
                    header.decompose()
                
                # Remove the section after header if it's the lead paragraph section
                section = soup.find('section', class_='py-4 bg-white')
                if section and 'lead' in str(section):
                    section.decompose()
            
            # Save the modified content
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(str(soup))
            print(f"Updated: {filename}")

if __name__ == "__main__":
    departments_dir = os.path.join(os.path.dirname(__file__), 'departments')
    remove_header_panel(departments_dir)
