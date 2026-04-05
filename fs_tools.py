import os
import datetime
from pathlib import Path

def read_file(filepath: str) -> dict:
    """
    Read resume files (PDF, TXT, DOCX), extract text content, and return structured response.
    """
    if not os.path.exists(filepath):
        return {"status": "error", "message": f"File not found: {filepath}", "content": None}

    ext = os.path.splitext(filepath)[1].lower()
    text = ""
    try:
        if ext == ".txt":
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                text = f.read()
        elif ext == ".pdf":
            import PyPDF2
            with open(filepath, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        elif ext == ".docx":
            import docx
            doc = docx.Document(filepath)
            text = "\n".join([para.text for para in doc.paragraphs])
        else:
            return {"status": "error", "message": f"Unsupported file type: {ext}", "content": None}
            
        file_stat = os.stat(filepath)
        metadata = {
            "filename": os.path.basename(filepath),
            "size_bytes": file_stat.st_size,
            "modified_time": datetime.datetime.fromtimestamp(file_stat.st_mtime).isoformat()
        }
        
        return {
            "status": "success",
            "metadata": metadata,
            "content": text
        }
    except Exception as e:
        return {"status": "error", "message": str(e), "content": None}

def list_files(directory: str, extension: str = None) -> list:
    """
    List all files in a directory, optionally filtering by extension.
    """
    if not os.path.exists(directory):
        return []
    
    file_list = []
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if extension and not file.lower().endswith(extension.lower()):
                    continue
                    
                filepath = os.path.join(root, file)
                file_stat = os.stat(filepath)
                file_list.append({
                    "name": file,
                    "path": filepath,
                    "size_bytes": file_stat.st_size,
                    "modified_time": datetime.datetime.fromtimestamp(file_stat.st_mtime).isoformat()
                })
        return file_list
    except Exception as e:
        print(f"Error listing files: {e}")
        return []

def write_file(filepath: str, content: str) -> dict:
    """
    Write content to file, creating directories if needed.
    """
    try:
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return {"status": "success", "message": f"Successfully wrote to {filepath}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def search_in_file(filepath: str, keyword: str) -> dict:
    """
    Search for keyword in file content, returning matches with context (case-insensitive).
    """
    read_result = read_file(filepath)
    if read_result["status"] == "error":
        return read_result
        
    text = read_result["content"]
    if not text:
        return {"status": "success", "matches": []}
        
    lines = text.split('\n')
    keyword_lower = keyword.lower()
    matches = []
    
    for i, line in enumerate(lines):
        if keyword_lower in line.lower():
            # Get some context (1 line before and after if available)
            start_idx = max(0, i - 1)
            end_idx = min(len(lines), i + 2)
            context = "\n".join(lines[start_idx:end_idx])
            matches.append({
                "line_number": i + 1,
                "matched_text": line.strip(),
                "context": context.strip()
            })
            
    return {
        "status": "success",
        "keyword": keyword,
        "matches_count": len(matches),
        "matches": matches
    }
