from pathlib import Path

from agent_learning_hub import content


def test_content_cli_reports_when_checkout_is_missing(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.chdir(tmp_path)
    assert content.main() == 2
    assert "source checkout" in capsys.readouterr().err


def test_content_cli_runs_from_repository_checkout(monkeypatch) -> None:
    root = Path(__file__).parents[2]
    monkeypatch.chdir(root)
    assert content.main() == 0
