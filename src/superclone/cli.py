import sys
from pathlib import Path
import click
from src.superclone.superclone import (
    clone_repository,
    build_context_from_repo,
    generate_summary,
    write_summary_and_gitignore,
    check_ollama_available
)
from .config import config


@click.command()
@click.argument("repo_url")
@click.option(
    "--target", "-t",
    default=".",
    type=click.Path(file_okay=False, writable=True, path_type=Path),
    help="Directory to clone into (default: current directory)"
)
@click.option(
    "--model", "-m",
    default=None,
    help=f"Ollama model to use (default: {config.OLLAMA_MODEL})"
)
@click.option(
    "--max-file-size",
    type=int,
    default=None,
    help=f"Max file size in KB to include (default: {config.MAX_FILE_SIZE_KB})"
)
@click.option(
    "--max-context-chars",
    type=int,
    default=None,
    help=f"Max context length in characters (default: {config.MAX_CONTEXT_CHARS})"
)
def main(repo_url: str, target: Path, model: str, max_file_size: int, max_context_chars: int):
    """
    Superclone: Clone a Git repository and generate an AI_doc.md summary using Ollama.

    REPO_URL: Git repository URL (e.g., https://github.com/user/repo.git)
    """
    # Override config with CLI options if provided
    if max_file_size is not None:
        config.MAX_FILE_SIZE_KB = max_file_size
    if max_context_chars is not None:
        config.MAX_CONTEXT_CHARS = max_context_chars

    # Determine the target directory (repo name extracted from URL)
    repo_name = Path(repo_url).stem
    clone_dir = (target / repo_name).resolve()

    click.echo("Checking Ollama availability...")
    available, message = check_ollama_available(model or config.OLLAMA_MODEL)
    if not available:
        click.echo(f"Ollama check failed: {message}", err=True)
        sys.exit(1) 

    if clone_dir.exists():
        click.confirm(f"Directory {clone_dir} already exists. Overwrite?", abort=True)
        import shutil
        shutil.rmtree(clone_dir)

    click.echo(f"Cloning {repo_url} into {clone_dir}...")
    try:
        clone_repository(repo_url, clone_dir)
    except Exception as e:
        click.echo(f"Clone failed: {e}", err=True)
        sys.exit(1)

    click.echo("Building context from repository files...")
    context = build_context_from_repo(clone_dir)
    if not context:
        click.echo("No readable text content found in repository.", err=True)
        sys.exit(1)

    click.echo(f"Generating summary using Ollama model '{model or config.OLLAMA_MODEL}'...")
    try:
        summary = generate_summary(context, model)
    except Exception as e:
        click.echo(f"Ollama generation failed: {e}", err=True)
        sys.exit(1)

    click.echo("Writing AI_doc.md and updating .gitignore...")
    write_summary_and_gitignore(clone_dir, summary)

    click.echo(f"✅ Done! Summary written to {clone_dir / 'AI_doc.md'}")
