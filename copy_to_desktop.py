"""
Copy Current SCIM OAuth Project to Desktop/IGA and Create ZIP
"""

import shutil
import zipfile
import os
from pathlib import Path
from datetime import datetime

def copy_and_zip_project():
    # Source directory
    source_dir = Path(r"c:\iga project")
    
    # Desktop path
    desktop = Path.home() / "Desktop"
    
    # Destination directory
    dest_dir = desktop / "IGA"
    
    # ZIP file path
    zip_path = desktop / "IGA.zip"
    
    # Files/folders to include (current project only)
    include_items = [
        'django_scim',
        'slack_scim',
        'pam',
        'manage.py',
        'start_servers.bat',
        'scim.db',
        'README.md',
        'COMPLETE_DOCUMENTATION.md',
        'requirements.txt',
        'django_requirements.txt'
    ]
    
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
    
    print("="*60)
    print("📦 SCIM OAuth Project - Copy & ZIP")
    print("="*60)
    print(f"\nSource: {source_dir}")
    print(f"Destination: {dest_dir}")
    print(f"ZIP File: {zip_path}")
    
    # Step 1: Remove old IGA folder if exists
    if dest_dir.exists():
        print(f"\n🗑️  Removing old IGA folder...")
        shutil.rmtree(dest_dir)
    
    # Step 2: Create new IGA folder
    print(f"\n📁 Creating IGA folder on Desktop...")
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    # Step 3: Copy files
    print(f"\n📋 Copying files...")
    copied_count = 0
    
    for item in include_items:
        source_item = source_dir / item
        dest_item = dest_dir / item
        
        if not source_item.exists():
            print(f"  ⚠️  Skipping (not found): {item}")
            continue
        
        if source_item.is_file():
            # Copy file
            shutil.copy2(source_item, dest_item)
            copied_count += 1
            print(f"  ✓ Copied: {item}")
        
        elif source_item.is_dir():
            # Copy directory
            shutil.copytree(
                source_item, 
                dest_item,
                ignore=shutil.ignore_patterns(*exclude_patterns)
            )
            copied_count += 1
            print(f"  ✓ Copied: {item}/ (folder)")
    
    # Step 4: Create ZIP file
    print(f"\n📦 Creating ZIP file...")
    
    # Remove old zip if exists
    if zip_path.exists():
        zip_path.unlink()
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        file_count = 0
        
        for root, dirs, files in os.walk(dest_dir):
            # Remove excluded directories
            dirs[:] = [d for d in dirs if not should_exclude(Path(root) / d)]
            
            for file in files:
                file_path = Path(root) / file
                
                # Skip excluded files
                if should_exclude(file_path):
                    continue
                
                # Calculate relative path
                rel_path = file_path.relative_to(dest_dir.parent)
                
                # Add to zip
                zipf.write(file_path, rel_path)
                file_count += 1
    
    # Get sizes
    folder_size = sum(f.stat().st_size for f in dest_dir.rglob('*') if f.is_file()) / (1024 * 1024)
    zip_size = zip_path.stat().st_size / (1024 * 1024)
    
    print("\n" + "="*60)
    print("✅ SUCCESS!")
    print("="*60)
    print(f"\n📁 Folder Created:")
    print(f"   Location: {dest_dir}")
    print(f"   Items: {copied_count}")
    print(f"   Size: {folder_size:.2f} MB")
    
    print(f"\n📦 ZIP Created:")
    print(f"   Location: {zip_path}")
    print(f"   Files: {file_count}")
    print(f"   Size: {zip_size:.2f} MB")
    
    print(f"\n🎉 Ready to use!")
    print(f"\nYou can find:")
    print(f"  - Folder: Desktop/IGA/")
    print(f"  - ZIP: Desktop/IGA.zip")

if __name__ == "__main__":
    try:
        copy_and_zip_project()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
