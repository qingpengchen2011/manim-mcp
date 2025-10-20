import os
import uuid
import shutil
from pathlib import Path
from typing import Dict, Optional

# Configuration
BASE_DIR = Path(__file__).parent.parent
UPLOAD_FOLDER = BASE_DIR / "uploads"
OUTPUT_FOLDER = BASE_DIR / "output"

# Ensure directories exist
UPLOAD_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)

def generate_id() -> str:
    """Generate a unique ID for file storage."""
    return str(uuid.uuid4())

def get_output_path(file_id: str) -> Path:
    """Get the path for an output file by ID."""
    return OUTPUT_FOLDER / f"{file_id}.mp4"

def get_upload_path(file_id: str) -> Path:
    """Get the path for an uploaded file by ID."""
    return UPLOAD_FOLDER / f"{file_id}.py"

def save_uploaded_file(file_id: str, content: str) -> Path:
    """Save uploaded Python code to a file."""
    file_path = get_upload_path(file_id)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return file_path

def cleanup_file(file_path: Path):
    """Remove a file if it exists."""
    if file_path.exists():
        file_path.unlink()

def cleanup_directory(directory: Path):
    """Remove a directory and all its contents."""
    if directory.exists() and directory.is_dir():
        shutil.rmtree(directory)
