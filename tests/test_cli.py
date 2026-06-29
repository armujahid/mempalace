import os
import sys
import types
from argparse import Namespace
from unittest.mock import Mock, patch

from mempalace import cli


def test_cmd_mcp_serve_sets_palace_env(monkeypatch):
    monkeypatch.delenv("MEMPALACE_PALACE_PATH", raising=False)
    fake_module = types.SimpleNamespace(main=Mock())
    monkeypatch.setitem(sys.modules, "mempalace.mcp_server", fake_module)

    cli.cmd_mcp_serve(Namespace(palace="~/palace-test"))

    assert os.environ["MEMPALACE_PALACE_PATH"] == os.path.abspath(os.path.expanduser("~/palace-test"))
    fake_module.main.assert_called_once_with()


def test_main_mcp_serve_palace_after_subcommand():
    with patch("sys.argv", ["mempalace", "mcp-serve", "--palace", "/tmp/palace"]), patch(
        "mempalace.cli.cmd_mcp_serve"
    ) as cmd:
        cli.main()
    assert cmd.call_args.args[0].palace == "/tmp/palace"


def test_main_mcp_serve_palace_before_subcommand():
    with patch("sys.argv", ["mempalace", "--palace", "/tmp/palace", "mcp-serve"]), patch(
        "mempalace.cli.cmd_mcp_serve"
    ) as cmd:
        cli.main()
    assert cmd.call_args.args[0].palace == "/tmp/palace"
