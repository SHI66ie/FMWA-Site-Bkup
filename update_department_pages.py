import os
import re

def update_department_page(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Update logo path and home link
    content = re.sub(
        r'<a class="navbar-brand d-flex align-items-center me-0" href="[^"]*">\s*<img src="[^"]*" alt="[^"]*" class="[^"]*">',
        '<a class="navbar-brand d-flex align-items-center me-0" href="../index.html">\n                <img src="../images/2025_07_14_13_42_IMG_2808.PNG" alt="Federal Ministry of Women Affairs Logo" class="fmwa-logo">',
        content
    )
    
    # Update navigation links
    content = re.sub(
        r'href="index.html"',
        'href="../index.html"',
        content
    )
    
    # Update about links
    content = re.sub(
        r'href="about.html',
        'href="../about.html',
        content
    )
    
    # Update organogram link
    content = re.sub(
        r'href="organogram.html"',
        'href="../organogram.html"',
        content
    )
    
    # Update department links
    content = re.sub(
        r'href="departments/([^"]+)"',
        r'href="../departments/\1"',
        content
    )
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def main():
    departments_dir = os.path.join(os.path.dirname(__file__), 'departments')
    
    for filename in os.listdir(departments_dir):
        if filename.endswith('.html'):
            file_path = os.path.join(departments_dir, filename)
            print(f"Updating {filename}...")
            update_department_page(file_path)
    
    print("All department pages have been updated successfully!")

if __name__ == "__main__":
    main()
