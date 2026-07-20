import importlib.util
import json
import subprocess
import sys
from pathlib import Path

PATH = Path(__file__).parents[1] / "solution" / "checklist.py"
SPEC = importlib.util.spec_from_file_location("lab_s09_checklist", PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_capstone_manifest_requires_release_and_safety_fields() -> None:
    manifest = {field: "synthetic" for field in MODULE.REQUIRED_FIELDS}
    assert MODULE.missing_fields(manifest) == set()
    manifest["permissions"] = ""
    assert MODULE.missing_fields(manifest) == {"permissions"}


def test_manifest_paths_directions_and_secret_like_values_are_validated(tmp_path) -> None:
    root = Path(__file__).parents[1]
    manifest = json.loads((root / "fixtures" / "manifest.json").read_text(encoding="utf-8"))
    assert MODULE.validate_manifest(manifest, root) == []
    manifest["direction"] = "unbounded-agent"
    manifest["eval_dataset"] = "../outside.json"
    manifest["logging"] = "token=do-not-store"
    issues = MODULE.validate_manifest(manifest, root)
    assert "invalid:direction" in issues
    assert "invalid:eval_dataset_path" in issues
    assert "secret_like_value" in issues


def test_local_capstone_cli_runs_fixed_eval_set_without_side_effects() -> None:
    root = Path(__file__).parents[1]
    completed = subprocess.run(  # noqa: S603 - fixed interpreter and repository fixture
        [sys.executable, str(root / "solution" / "demo.py")],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    report = json.loads(completed.stdout)
    assert report["passed"] == report["total"] == 5
    assert report["external_side_effects"] == 0
    assert {item["stop_reason"] for item in report["outcomes"]} >= {
        "complete",
        "no_sources",
        "permission_denied",
        "sensitive_input_rejected",
        "invalid_input",
    }


def test_all_three_directions_share_release_checklist() -> None:
    templates = Path(__file__).parents[1] / "solution" / "templates"
    assert (templates / "RELEASE_CHECKLIST.md").is_file()
    for name in (
        "research-assistant.md",
        "code-review-assistant.md",
        "personal-knowledge-assistant.md",
    ):
        assert "RELEASE_CHECKLIST.md" in (templates / name).read_text(encoding="utf-8")
