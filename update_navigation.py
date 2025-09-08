import os
from bs4 import BeautifulSoup

def update_navigation(directory):
    # Read the template file to get the updated navigation
    with open(os.path.join(directory, 'template.html'), 'r', encoding='utf-8') as f:
        template_soup = BeautifulSoup(f, 'html.parser')
    
    # Find the navigation in the template
    template_nav = template_soup.find('nav', class_='navbar')
    if not template_nav:
        print("Could not find navigation in template")
        return
    
    # Process each department HTML file
    for filename in os.listdir(directory):
        if filename.endswith('.html') and filename != 'template.html':
            filepath = os.path.join(directory, filename)
            print(f"Updating navigation in {filename}...")
            
            with open(filepath, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
            
            # Find and replace the navigation
            nav = soup.find('nav', class_='navbar')
            if nav:
                nav.replace_with(template_nav)
                
                # Update active state for the current department
                current_dept = filename.replace('.html', '').replace('-', ' ').title()
                for a in soup.find_all('a', class_='dropdown-item'):
                    if a.text.strip().lower() == current_dept.lower():
                        a.parent['class'] = a.parent.get('class', []) + ['active']
            
            # Save the updated file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(soup))

if __name__ == "__main__":
    departments_dir = os.path.join(os.path.dirname(__file__), 'departments')
    update_navigation(departments_dir)
