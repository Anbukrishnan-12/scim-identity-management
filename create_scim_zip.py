"""
Create ZIP file of SCIM OAuth Project ONLY
Excludes old projects and unnecessary files
"""

import zipfile
import os
from pathlib import Path
from datetime import datetime

def create_scim_oauth_zip():
    # Project directory
    project_dir = Path(r"c:\iga project")
    
    # Output zip file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_path = Path(rf"c:\scim-oauth-project_{timestamp}.zip")
    
    # ONLY include these folders/files (current project)
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
        '.env',
        'migrations/__pycache__'
    ]
    
    def should_exclude(path):
        """Check if path should be excluded"""
        path_str = str(path)
        for pattern in exclude_patterns:
            if pattern in path_str:
                return True
        return False
    
    print("="*60)
    print("📦 Creating SCIM OAuth Project ZIP")
    print("="*60)
    print(f"\nOutput: {zip_path}")
    print(f"Source: {project_dir}")
    
    print("\n✅ Including:")
    for item in include_items:
        print(f"  - {item}")
    
    print("\n❌ Excluding:")
    for pattern in exclude_patterns:
        print(f"  - {pattern}")
    
    print("\n🔄 Processing files...")
    
    # Create zip file
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        file_count = 0
        
        for item in include_items:
            item_path = project_dir / item
            
            if not item_path.exists():
                print(f"  ⚠️  Skipping (not found): {item}")
                continue
            
            # If it's a file
            if item_path.is_file():
                rel_path = Path("scim-oauth-project") / item
                zipf.write(item_path, rel_path)
                file_count += 1
                print(f"  ✓ Added: {item}")
            
            # If it's a directory
            elif item_path.is_dir():
                for root, dirs, files in os.walk(item_path):
                    # Remove excluded directories
                    dirs[:] = [d for d in dirs if not should_exclude(Path(root) / d)]
                    
                    for file in files:
                        file_path = Path(root) / file
                        
                        # Skip excluded files
                        if should_exclude(file_path):
                            continue
                        
                        # Calculate relative path
                        rel_path = Path("scim-oauth-project") / file_path.relative_to(project_dir)
                        
                        # Add to zip
                        zipf.write(file_path, rel_path)
                        file_count += 1
                
                print(f"  ✓ Added: {item}/ (folder)")
    
    # Get zip file size
    zip_size = zip_path.stat().st_size / (1024 * 1024)  # MB
    
    print("\n" + "="*60)
    print("✅ ZIP file created successfully!")
    print("="*60)
    print(f"📦 Location: {zip_path}")
    print(f"📊 Total files: {file_count}")
    print(f"💾 Size: {zip_size:.2f} MB")
    print("\n🎉 Ready to share!")

if __name__ == "__main__":
    try:
        create_scim_oauth_zip()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
