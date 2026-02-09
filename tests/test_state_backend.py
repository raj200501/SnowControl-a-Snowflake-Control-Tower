from pathlib import Path

from snowcontrol.core.state_backend import LocalStateBackend


def test_state_backend_apply(tmp_path: Path) -> None:
    backend = LocalStateBackend(tmp_path / "state.json")
    state = backend.load()
    assert state["state_version"] == 1
    backend.apply(
        [
            {
                "action": "CREATE",
                "resource_type": "warehouse",
                "name": "WH_TEST",
                "details": {"name": "WH_TEST"},
            }
        ]
    )
    state = backend.load()
    assert state["resources"]["warehouse"]["WH_TEST"]["name"] == "WH_TEST"
