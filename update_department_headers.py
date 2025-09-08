import os
import re
from bs4 import BeautifulSoup, element

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

def add_title_bar(soup, department_name):
    """Add title bar with breadcrumb navigation to the department page."""
    # Create the title bar div
    title_bar = soup.new_tag('div', **{'class': 'department-title-bar'})
    container = soup.new_tag('div', **{'class': 'container'})
    title_bar.append(container)
    
    # Create the flex container
    flex_div = soup.new_tag('div', **{
        'class': 'd-flex justify-content-between align-items-center'
    })
    container.append(flex_div)
    
    # Add the title
    title = soup.new_tag('h1', **{'class': 'department-title mb-0'})
    title.string = department_name
    flex_div.append(title)
    
    # Create the breadcrumb navigation
    nav = soup.new_tag('nav', **{'aria-label': 'breadcrumb'})
    breadcrumb = soup.new_tag('ol', **{'class': 'breadcrumb mb-0'})
    nav.append(breadcrumb)
    
    # Add breadcrumb items
    def add_breadcrumb_item(text, href=None, active=False):
        item = soup.new_tag('li', **{'class': 'breadcrumb-item'})
        if active:
            item['class'].append('active')
            item['aria-current'] = 'page'
            item.string = text
        else:
            link = soup.new_tag('a', href=href)
            link.string = text
            item.append(link)
        breadcrumb.append(item)
    
    add_breadcrumb_item('Home', '../index.html')
    add_breadcrumb_item('Departments', '#')
    add_breadcrumb_item(department_name, active=True)
    
    flex_div.append(nav)
    
    # Find the main content and insert the title bar before it
    main_content = soup.find('main')
    if main_content:
        main_content.insert_before(title_bar)
    
    return soup

def update_department_pages(directory):
    """Update all department pages with the title bar."""
    for filename, dept_name in department_names.items():
        filepath = os.path.join(directory, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
                
                # Skip if title bar already exists
                if 'department-title-bar' in content:
                    print(f"Skipping {filename} - already has title bar")
                    continue
                
                # Parse with html.parser for better handling of malformed HTML
                soup = BeautifulSoup(content, 'html.parser')
                
                # Add the title bar
                soup = add_title_bar(soup, dept_name)
                
                # Pretty-print the HTML with proper indentation
                pretty_html = soup.prettify()
                
                # Fix any HTML entities that were converted
                pretty_html = pretty_html.replace('&amp;', '&')
                
                # Save the updated content with proper formatting
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(pretty_html)
                
                print(f"Updated: {filename}")

if __name__ == "__main__":
    departments_dir = os.path.join(os.path.dirname(__file__), 'departments')
    update_department_pages(departments_dir)
