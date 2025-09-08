import os
import re
from bs4 import BeautifulSoup

# Department names mapping
department_names = {
    'child-development.html': 'Child Development',
    'community-development-social-intervention.html': 'Community Development & Social Intervention',
    'finance-accounting.html': 'Finance & Accounting',
    'gender-affairs.html': 'Gender Affairs',
    'general-services.html': 'General Services',
    'nutrition.html': 'Nutrition',
    'planning-research-statistics.html': 'Planning, Research & Statistics',
    'procurement.html': 'Procurement',
    'reform-coordination-service-improvement.html': 'Reform Coordination & Service Improvement',
    'women-development.html': 'Women Development'
}

def update_department_title(file_path, department_name):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Replace the department name placeholders
    updated_content = content.replace('{{DEPARTMENT_NAME}}', department_name)
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)

def main():
    departments_dir = os.path.join(os.path.dirname(__file__), 'departments')
    
    # First, update the template with a generic placeholder
    template_path = os.path.join(departments_dir, 'template.html')
    
    # Then update each department page
    for filename, dept_name in department_names.items():
        file_path = os.path.join(departments_dir, filename)
        if os.path.exists(file_path):
            print(f"Updating {filename}...")
            update_department_title(file_path, dept_name)
    
    print("Department title updates complete!")

if __name__ == "__main__":
    main()
