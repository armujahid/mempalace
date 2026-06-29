import json
import os
import stat
import subprocess
import sys
from pathlib import Path

from mempalace.hooks import hook_path, hooks_dir


def run_cli(*args):
    return subprocess.run(
        [sys.executable, "-m", "mempalace", *args],
        check=True,
        capture_output=True,
        text=True,
    )


def test_hooks_dir_points_to_package():
    path = hooks_dir()
    assert path.is_dir()
    assert str(path).endswith("mempalace/hooks")


def test_hook_path_resolves_known_hooks():
    assert hook_path("save").name == "mempal_save_hook.sh"
    assert hook_path("precompact").name == "mempal_precompact_hook.sh"


def test_hook_scripts_are_executable():
    for name in ("save", "precompact"):
        mode = hook_path(name).stat().st_mode
        assert mode & stat.S_IXUSR


def test_cli_hooks_path():
    result = run_cli("hooks", "path")
    assert result.stdout.strip().endswith("mempalace/hooks")


def test_cli_hooks_path_specific_hook():
    result = run_cli("hooks", "path", "save")
    assert result.stdout.strip().endswith("mempalace/hooks/mempal_save_hook.sh")


def test_cli_hooks_install_claude_outputs_json_stdout():
    result = run_cli("hooks", "install")
    config = json.loads(result.stdout)
    assert "Add to .claude/settings.local.json" in result.stderr
    assert config["hooks"]["Stop"][0]["hooks"][0]["command"].endswith("mempal_save_hook.sh")
    assert config["hooks"]["PreCompact"][0]["hooks"][0]["command"].endswith(
        "mempal_precompact_hook.sh"
    )


def test_cli_hooks_install_codex_outputs_json_stdout():
    result = run_cli("hooks", "install", "--format", "codex")
    config = json.loads(result.stdout)
    assert "Add to .codex/hooks.json" in result.stderr
    assert config["Stop"][0]["command"].endswith("mempal_save_hook.sh")
    assert config["PreCompact"][0]["command"].endswith("mempal_precompact_hook.sh")
