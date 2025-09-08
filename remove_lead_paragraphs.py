import os
from bs4 import BeautifulSoup

def remove_lead_paragraphs(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.html') and filename != 'template.html':
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'html.parser')
                
                # Find and remove the lead paragraph in the header
                header = soup.find('header', class_='department-header')
                if header:
                    lead_para = header.find('p', class_='lead')
                    if lead_para:
                        lead_para.decompose()
            
            # Save the modified content
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(str(soup))
            print(f"Updated: {filename}")

if __name__ == "__main__":
    departments_dir = os.path.join(os.path.dirname(__file__), 'departments')
    remove_lead_paragraphs(departments_dir)
