"""Installed MemPalace hook script resources."""

from importlib import resources
from pathlib import Path

HOOK_FILES = {
    "save": "mempal_save_hook.sh",
    "precompact": "mempal_precompact_hook.sh",
}


def hooks_dir() -> Path:
    """Return the installed directory containing MemPalace hook scripts."""
    return Path(str(resources.files(__package__)))


def hook_path(name: str) -> Path:
    """Return the path to a bundled hook script by name or filename."""
    filename = HOOK_FILES.get(name, name)
    if filename not in HOOK_FILES.values():
        raise ValueError(f"Unknown hook: {name}")
    return hooks_dir() / filename
