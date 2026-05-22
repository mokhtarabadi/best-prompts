#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pathspec",
#     "mcp[cli]"
# ]
# ///

import os
import sys
from pathlib import Path
from typing import Optional

import pathspec
from mcp.server.fastmcp import FastMCP

class GitIgnoreFilter:
    """Evaluates paths against .gitignore files dynamically."""
    def __init__(self) -> None:
        self._specs: dict[Path, Optional[pathspec.PathSpec]] = {}

    def _get_spec(self, dir_path: Path) -> Optional[pathspec.PathSpec]:
        if dir_path in self._specs:
            return self._specs[dir_path]
        gitignore_file = dir_path / ".gitignore"
        if gitignore_file.is_file():
            try:
                with open(gitignore_file, "r", encoding="utf-8") as f:
                    spec = pathspec.PathSpec.from_lines("gitwildmatch", f)
                    self._specs[dir_path] = spec
                    return spec
            except Exception as e:
                print(f"Warning: Failed to read {gitignore_file}: {e}", file=sys.stderr)
        self._specs[dir_path] = None
        return None

    def is_ignored(self, path: Path) -> bool:
        abs_path = path.resolve()
        if ".git" in abs_path.parts or abs_path.name == ".git":
            return True
        current = abs_path.parent
        while True:
            spec = self._get_spec(current)
            if spec:
                try:
                    rel_path = abs_path.relative_to(current)
                    match_str = rel_path.as_posix()
                    if abs_path.is_dir() and not match_str.endswith("/"):
                        match_str += "/"
                    if spec.match_file(match_str):
                        return True
                except ValueError:
                    pass
            if current == current.parent:
                break
            current = current.parent
        return False

def is_binary(file_path: Path) -> bool:
    try:
        with open(file_path, "rb") as f:
            chunk = f.read(1024)
            if b"\0" in chunk:
                return True
            chunk.decode("utf-8")
            return False
    except Exception:
        return True

def generate_tree(dir_path: Path, ignore_filter: GitIgnoreFilter) -> str:
    lines = ["```text", dir_path.name or str(dir_path)]
    def _walk(current_path: Path, prefix: str) -> None:
        try:
            entries = list(current_path.iterdir())
        except PermissionError:
            lines.append(f"{prefix}└── [Permission Denied]")
            return
        valid_entries = [e for e in entries if not ignore_filter.is_ignored(e)]
        sorted_entries = sorted(valid_entries, key=lambda e: (not e.is_dir(), e.name.lower()))
        for i, entry in enumerate(sorted_entries):
            is_last = i == (len(sorted_entries) - 1)
            connector = "└── " if is_last else "├── "
            lines.append(f"{prefix}{connector}{entry.name}")
            if entry.is_dir():
                extension = "    " if is_last else "│   "
                _walk(entry, prefix + extension)
    _walk(dir_path, "")
    lines.append("```")
    return "\n".join(lines)

def process_source_file(file_path: Path, max_size: int, line_numbers: bool) -> str:
    lines = [f"### `{file_path}`", ""]
    if not file_path.exists():
        lines.append("> Skipped: (File not found)\n")
        return "\n".join(lines)
    try:
        size = file_path.stat().st_size
        if size > max_size:
            lines.append(f"> Skipped: (File too large: {size} bytes)\n")
            return "\n".join(lines)
    except OSError as e:
        lines.append(f"> Skipped: (OS Error: {e})\n")
        return "\n".join(lines)
    if is_binary(file_path):
        lines.append("> Skipped: (Binary file)\n")
        return "\n".join(lines)
    ext = file_path.suffix.lstrip(".") or "text"
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            file_lines = f.read().split("\n")
        if file_lines and file_lines[-1] == "":
            file_lines.pop()
        if line_numbers:
            content = "\n".join(f"{i}: {line}" for i, line in enumerate(file_lines, 1))
        else:
            content = "\n".join(file_lines)
        lines.append(f"```{ext}")
        if content:
            lines.append(content)
        lines.append("```\n")
    except Exception as e:
        lines.append(f"> Skipped: (Error reading file: {e})\n")
    return "\n".join(lines)

def collect_files(target: str, ignore_filter: GitIgnoreFilter) -> list[Path]:
    p = Path(target)
    if not p.exists() or ignore_filter.is_ignored(p):
        return []
    if p.is_file():
        return [p]
    collected = []
    for root, dirs, files in os.walk(p):
        root_path = Path(root)
        dirs[:] = [d for d in dirs if not ignore_filter.is_ignored(root_path / d)]
        for f in files:
            file_path = root_path / f
            if not ignore_filter.is_ignored(file_path):
                collected.append(file_path)
    return collected

mcp = FastMCP("CustomContext")

@mcp.tool()
def get_directory_tree(target_path: str = ".") -> str:
    """Generates an ASCII tree representation of the directory, respecting .gitignore. Use this to discover codebase structure."""
    ignore_filter = GitIgnoreFilter()
    tree_path = Path(target_path)
    if not tree_path.is_dir():
        return f"Error: {target_path} is not a valid directory."
    if ignore_filter.is_ignored(tree_path):
        return f"Warning: Target tree path is ignored by .gitignore: {target_path}"
    return f"## Directory Tree: `{tree_path}`\n\n" + generate_tree(tree_path, ignore_filter)

@mcp.tool()
def read_source_files(paths: list[str], max_size: int = 1048576, no_line_numbers: bool = False) -> str:
    """Reads multiple source files or directories and returns their contents in markdown, respecting .gitignore. Returns line numbers by default."""
    ignore_filter = GitIgnoreFilter()
    files_to_process: dict[Path, Path] = {}
    for src in paths:
        for p in collect_files(src, ignore_filter):
            files_to_process[p.resolve()] = p
    if not files_to_process:
        return "No files found or all files were ignored."
    output_lines = ["## Source Files\n"]
    include_line_numbers = not no_line_numbers
    for _, f in sorted(files_to_process.items(), key=lambda item: str(item[1]).lower()):
        output_lines.append(process_source_file(f, max_size, include_line_numbers))
    return "\n".join(output_lines)

if __name__ == "__main__":
    mcp.run(transport="stdio")
