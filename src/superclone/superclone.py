import subprocess
from pathlib import Path
from typing import Optional
import ollama
from .config import config


def check_ollama_available(model: str) -> tuple[bool, str]:
    """
    Check if Ollama server is reachable and the specified model exists.

    Returns:
        Tuple of (success, error_message)
    """
    try:
        # First try to list models (basic connectivity test)
        models_response = ollama.list()
        available_models = [m["name"] for m in models_response.get("models", [])]
        # Also check with the exact tag (e.g., "llama3:latest")
        model_base = model.split(":")[0]
        if model in available_models or model_base in available_models:
            return True, ""
        else:
            return False, f"Model '{model}' not found. Pull it with: ollama pull {model}"
    except Exception as e:
        return False, f"Cannot connect to Ollama: {e}\nMake sure Ollama is running (ollama serve)."
    
def clone_repository(repo_url: str, target_dir: Path) -> None:
    """Clone a Git repository into target_dir (creates subdir with repo name)."""
    if not target_dir.exists():
        target_dir.mkdir(parents=True)
    subprocess.run(
        ["git", "clone", repo_url, str(target_dir)],
        check=True,
        capture_output=True,
        text=True
    )

def is_likely_binary(file_path: Path) -> bool:
    """Check if a file is likely binary."""
    if file_path.suffix.lower() in config.BINARY_EXTENSIONS:
        return True
    try:
        with open(file_path, "rb") as f:
            chunk = f.read(1024)
            return b"\x00" in chunk
    except Exception:
        return True

def build_context_from_repo(repo_root: Path) -> str:
    """Walk the repo, collect text file contents, return formatted string."""
    context_parts = ["# Repository File Contents\n"]
    total_chars = 0

    for file_path in repo_root.rglob("*"):
        if file_path.is_file() and ".git" not in file_path.parts:
            if is_likely_binary(file_path):
                continue
            size = file_path.stat().st_size
            if size > config.MAX_FILE_SIZE_KB * 1024:
                rel_path = file_path.relative_to(repo_root)
                context_parts.append(f"\n## {rel_path}\n[File too large, skipped]\n")
                continue
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                rel_path = file_path.relative_to(repo_root)
                context_parts.append(f"\n## {rel_path}\n```\n{content}\n```\n")
                total_chars += len(content)
                if total_chars > config.MAX_CONTEXT_CHARS:
                    context_parts.append("\n[Context truncated due to size limit]\n")
                    break
            except Exception:
                continue
    return "".join(context_parts)

def generate_summary(context: str, model: Optional[str] = None) -> str:
    """Send context to Ollama and return Markdown summary."""
    model = model or config.OLLAMA_MODEL
    prompt = f"""
You are an AI assistant that summarizes Git repositories.
Given the following file contents from a repository, provide a comprehensive summary that includes:
- Purpose and main functionality of the project
- Key technologies and languages used
- High-level architecture / important modules
- Notable dependencies
- Any other relevant observations

Repository contents:
{context}

Provide the summary in Markdown format.
"""
    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]

def write_summary_and_gitignore(repo_path: Path, summary: str) -> None:
    """Write AI_doc.md and ensure it's in .gitignore."""
    doc_path = repo_path / "AI_doc.md"
    doc_path.write_text(summary, encoding="utf-8")

    gitignore_path = repo_path / ".gitignore"
    lines = gitignore_path.read_text(encoding="utf-8").splitlines() if gitignore_path.exists() else []
    if "AI_doc.md" not in lines:
        with gitignore_path.open("a", encoding="utf-8") as f:
            f.write("\nAI_doc.md\n")