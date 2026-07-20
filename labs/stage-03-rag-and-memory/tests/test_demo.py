import importlib.util
import json
from pathlib import Path

from agent_learning_hub.retrieval import validate_claim_citations

PATH = Path(__file__).parents[1] / "solution" / "demo.py"
SPEC = importlib.util.spec_from_file_location("lab_s03_demo", PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_chinese_retrieval_and_cross_process_store(tmp_path) -> None:
    fixtures = PATH.parents[1] / "fixtures"
    queries = json.loads((fixtures / "queries.json").read_text(encoding="utf-8"))
    for case in queries:
        result = MODULE.build_index().search(case["query"], threshold=0.05)
        assert [item.chunk.id for item in result[:1]] == case["expected_chunk_ids"]
    path = tmp_path / "memory.sqlite3"
    store = MODULE.open_synthetic_memory(path)
    store.write("preference", "合成学习者偏好离线实验", source="fixture")
    reopened = MODULE.open_synthetic_memory(path)
    assert reopened.get("preference").content == "合成学习者偏好离线实验"
    assert reopened.delete("preference")
    assert reopened.get("preference") is None


def test_fixed_human_annotations_check_claim_support() -> None:
    fixtures = PATH.parents[1] / "fixtures"
    case = json.loads((fixtures / "citation-cases.json").read_text(encoding="utf-8"))
    chunks = {result.chunk.id: result.chunk.text for result in MODULE.build_index().search("记忆")}
    chunks.update(
        {result.chunk.id: result.chunk.text for result in MODULE.build_index().search("检索")}
    )
    issues = validate_claim_citations(
        case["claims"],
        case["citations"],
        chunks,
        set(case["required_claim_ids"]),
        {tuple(pair) for pair in case["supported_pairs"]},
    )
    assert [[issue.claim_id, issue.code] for issue in issues] == case["expected_issues"]
