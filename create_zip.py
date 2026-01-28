"""
Create ZIP file of the project
Excludes unnecessary files like __pycache__, .pyc, etc.
"""

import zipfile
import os
from pathlib import Path

def create_project_zip():
    # Project directory
    project_dir = Path(r"c:\iga project")
    
    # Output zip file
    zip_path = Path(r"c:\iga-project.zip")
    
    # Files/folders to exclude
    exclude_patterns = [
        '__pycache__',
        '*.pyc',
        '*.pyo',
        '.git',
        '.vscode',
        '.idea',
        '*.log',
        'venv',
        'env',
        '.env'
    ]
    
    def should_exclude(path):
        """Check if path should be excluded"""
        path_str = str(path)
        for pattern in exclude_patterns:
            if pattern in path_str:
                return True
        return False
    
    print(f"Creating ZIP file: {zip_path}")
    print(f"Source: {project_dir}")
    print("\nExcluding:")
    for pattern in exclude_patterns:
        print(f"  - {pattern}")
    print("\nProcessing files...")
    
    # Create zip file
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        file_count = 0
        
        # Walk through directory
        for root, dirs, files in os.walk(project_dir):
            # Remove excluded directories
            dirs[:] = [d for d in dirs if not should_exclude(Path(root) / d)]
            
            for file in files:
                file_path = Path(root) / file
                
                # Skip excluded files
                if should_exclude(file_path):
                    continue
                
                # Calculate relative path
                rel_path = file_path.relative_to(project_dir.parent)
                
                # Add to zip
                zipf.write(file_path, rel_path)
                file_count += 1
                
                if file_count % 10 == 0:
                    print(f"  Added {file_count} files...")
    
    # Get zip file size
    zip_size = zip_path.stat().st_size / (1024 * 1024)  # MB
    
    print(f"\n✅ ZIP file created successfully!")
    print(f"📦 Location: {zip_path}")
    print(f"📊 Total files: {file_count}")
    print(f"💾 Size: {zip_size:.2f} MB")

if __name__ == "__main__":
    try:
        create_project_zip()
    except Exception as e:
        print(f"\n❌ Error: {e}")
