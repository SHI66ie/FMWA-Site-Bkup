import os
import re

def update_logo_paths(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.html'):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # Update favicon path
                content = re.sub(
                    r'<link rel="icon"[^>]*?href=["\'](.*?logo-removebg-preview\.png)["\']',
                    '<link rel="icon" type="image/png" href="../images/2025_07_14_13_42_IMG_2808.PNG"',
                    content
                )
                
                # Update logo in navigation
                content = re.sub(
                    r'<img[^>]*?src=["\'](.*?logo-removebg-preview\.png)["\'][^>]*>',
                    '<img src="../images/2025_07_14_13_42_IMG_2808.PNG" alt="Federal Ministry of Women Affairs Logo" class="fmwa-logo">',
                    content
                )
                
                # Update new logo path if it's incorrect
                content = re.sub(
                    r'<img[^>]*?src=["\'](?!\.\./)(?:images/)?(2025_07_14_13_42_IMG_2808\.PNG)["\']',
                    '<img src="../images/2025_07_14_13_42_IMG_2808.PNG" alt="Federal Ministry of Women Affairs Logo" class="fmwa-logo">',
                    content
                )
                
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"Updated: {filename}")
                
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    departments_dir = os.path.join(os.path.dirname(__file__), 'departments')
    update_logo_paths(departments_dir)
