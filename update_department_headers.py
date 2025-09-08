import os
import re
from bs4 import BeautifulSoup, element

# Department names and slogans mapping
department_info = {
    'child-development.html': {
        'name': 'Child Development',
        'slogan': 'Protecting and Empowering Every Nigerian Child'
    },
    'community-development-social-intervention.html': {
        'name': 'Community Development & Social Intervention',
        'slogan': 'Empowering Communities, Transforming Lives'
    },
    'finance-accounting.html': {
        'name': 'Finance & Accounting',
        'slogan': 'Ensuring Financial Integrity and Accountability'
    },
    'gender-affairs.html': {
        'name': 'Gender Affairs',
        'slogan': 'Promoting Gender Equality and Women\'s Empowerment'
    },
    'general-services.html': {
        'name': 'General Services',
        'slogan': 'Delivering Excellence in Administrative Support'
    },
    'nutrition.html': {
        'name': 'Nutrition',
        'slogan': 'Nourishing the Nation, Building a Healthier Future'
    },
    'planning-research-statistics.html': {
        'name': 'Planning, Research & Statistics',
        'slogan': 'Informing Policy Through Data and Analysis'
    },
    'procurement.html': {
        'name': 'Procurement',
        'slogan': 'Ensuring Transparency and Efficiency in Procurement'
    },
    'reform-coordination-service-improvement.html': {
        'name': 'Reform Coordination & Service Improvement',
        'slogan': 'Driving Innovation and Excellence in Public Service'
    },
    'women-development.html': {
        'name': 'Women Development',
        'slogan': 'Empowering Women, Strengthening the Nation'
    }
}

def add_title_bar(soup, department_info):
    """Add title bar with department name and slogan to the department page."""
    # Create the title bar div
    title_bar = soup.new_tag('div', **{'class': 'department-title-bar'})
    container = soup.new_tag('div', **{'class': 'container'})
    title_bar.append(container)
    
    # Create the title container
    title_container = soup.new_tag('div', **{'class': 'text-center'})
    container.append(title_container)
    
    # Add the title
    title = soup.new_tag('h1', **{'class': 'department-title mb-1'})
    title.string = department_info['name']
    title_container.append(title)
    
    # Add the slogan if it exists
    if 'slogan' in department_info and department_info['slogan']:
        slogan = soup.new_tag('div', **{'class': 'department-slogan'})
        slogan.string = department_info['slogan']
        title_container.append(slogan)
    
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
    add_breadcrumb_item(department_info['name'], active=True)
    
    container.append(nav)
    
    # Find the main content and insert the title bar before it
    main_content = soup.find('main')
    if main_content:
        main_content.insert_before(title_bar)
    
    return soup

def update_department_pages(directory):
    """Update all department pages with the title bar."""
    for filename, dept_info in department_info.items():
        filepath = os.path.join(directory, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
                
                # Skip if title bar already exists and has a slogan
                if 'department-slogan' in content:
                    print(f"Skipping {filename} - already has title bar with slogan")
                    continue
                
                soup = BeautifulSoup(content, 'html.parser')
                
                # Remove existing title bar if it exists
                existing_title_bar = soup.find('div', class_='department-title-bar')
                if existing_title_bar:
                    existing_title_bar.decompose()
                
                # Add the title bar with slogan
                soup = add_title_bar(soup, dept_info)
                
                # Add dropdown-styles.css if not already present
                head = soup.find('head')
                if head:
                    # Check if the stylesheet is already linked
                    if not head.find('link', {'href': '../css/dropdown-styles.css'}):
                        link_tag = soup.new_tag('link', rel='stylesheet', href='../css/dropdown-styles.css')
                        head.append(link_tag)
                
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
