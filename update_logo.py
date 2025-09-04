import os
import re

def update_logo_in_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Update favicon
        content = re.sub(
            r'<link rel="icon"[^>]*?href=["\'](.*?logo-removebg-preview\.png)["\']',
            '<link rel="icon" type="image/png" href="images/2025_07_14_13_42_IMG_2808.PNG"',
            content
        )
        
        # Update logo in header
        content = re.sub(
            r'<img[^>]*?src=["\'](.*?logo-removebg-preview\.png)["\'][^>]*>',
            '<img src="../images/2025_07_14_13_42_IMG_2808.PNG" alt="Federal Ministry of Women Affairs Logo" class="fmwa-logo">',
            content
        )
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Updated: {file_path}")
        return True
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return False

def main():
    # Get all HTML files
    html_files = []
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    # Update each file
    updated = 0
    for file_path in html_files:
        if update_logo_in_file(file_path):
            updated += 1
    
    print(f"\nSuccessfully updated {updated} files.")

if __name__ == "__main__":
    main()
