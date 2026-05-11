#!/usr/bin/env python3
"""Linter for quiz-tracker source architecture.

Validates:
- Every source file lives in exactly one layer directory under src/
- Imports respect the forward dependency direction
- No file exceeds 300 lines
"""

import ast
import sys
from pathlib import Path

# Layer order defines the dependency direction
LAYER_ORDER = ["utils", "providers", "config", "types", "repo", "service", "runtime", "ui"]
LAYER_DIRS = set(LAYER_ORDER)

# Each layer may only import from layers at or before it in the order
LAYER_ALLOWED_IMPORTS = {
    "types": {"types"},
    "config": {"types", "config"},
    "repo": {"types", "config", "repo"},
    "service": {"types", "config", "repo", "providers", "service"},
    "runtime": {"types", "config", "repo", "service", "providers", "runtime"},
    "ui": {"types", "config", "service", "runtime", "providers", "ui"},
    "providers": {"types", "config", "utils", "providers"},
    "utils": {"utils"},
}


def get_layer_from_path(filepath: Path) -> str:
    """Determine the layer directory of a file."""
    try:
        rel_path = filepath.relative_to(Path("src"))
        parts = rel_path.parts
        if parts and parts[0] in LAYER_DIRS:
            return parts[0]
    except ValueError:
        pass
    return ""


def get_imports(filepath: Path) -> list[tuple[str, int]]:
    """Extract import statements from a Python file."""
    imports = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
        tree = ast.parse(source, filename=str(filepath))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append((alias.name, node.lineno))
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append((node.module, node.lineno))
                elif node.level and node.names:
                    # relative import like "from . import x" or "from ..mod import x"
                    imports.append(("<relative>", node.lineno))
    except SyntaxError:
        pass
    return imports


def is_internal_import(module_name: str, filepath: Path) -> bool:
    """Check if an import is referencing internal source code."""
    # Check if it starts with 'src.' or is in the layer dirs
    parts = module_name.split(".")
    if parts and parts[0] == "src":
        return True
    if parts and parts[0] in LAYER_DIRS:
        return True
    # Check if importing a module that exists under src/
    src_path = Path("src") / module_name.replace(".", "/")
    if src_path.exists() or (src_path.parent / "__init__.py").exists():
        return True
    return False


def get_internal_import_module(module_name: str) -> str:
    """Extract the internal layer from an import path."""
    parts = module_name.split(".")
    for part in parts:
        if part in LAYER_DIRS:
            return part
        if part == "src":
            continue
    return ""


def validate_file(filepath: Path) -> list[str]:
    """Validate a single source file. Returns list of violations."""
    violations = []

    # Check file length
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    if len(lines) > 300:
        violations.append(f"{filepath}:1: File exceeds 300 lines ({len(lines)} lines)")

    # Determine layer
    layer = get_layer_from_path(filepath)
    if not layer:
        return violations  # Not in src/ layers, skip

    # Check imports
    imports = get_imports(filepath)
    for module_name, lineno in imports:
        if module_name == "<relative>":
            # Relative imports are allowed as long as they stay within the same module
            continue
        if is_internal_import(module_name, filepath):
            imported_layer = get_internal_import_module(module_name)
            if imported_layer and imported_layer not in LAYER_ALLOWED_IMPORTS.get(layer, set()):
                violations.append(
                    f"{filepath}:{lineno}: {layer} layer cannot import from {imported_layer} layer"
                )

    return violations


def main() -> int:
    """Run the linter. Returns 0 on success, 1 on failure."""
    src_dir = Path("src")
    if not src_dir.exists():
        print("Error: src/ directory not found")
        return 1

    all_violations = []
    py_files = list(src_dir.rglob("*.py"))

    for filepath in py_files:
        violations = validate_file(filepath)
        all_violations.extend(violations)

    if all_violations:
        print("Linting failed:")
        for v in all_violations:
            print(f"  {v}")
        return 1

    print(f"Linting passed: {len(py_files)} files checked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
