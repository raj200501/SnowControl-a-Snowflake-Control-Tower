from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory

import typer

from snowcontrol.config.loader import ConfigError, load_config
from snowcontrol.core.diff import diff_state
from snowcontrol.core.plan import actions_to_payload
from snowcontrol.core.policies.builtin import BUILTIN_POLICIES
from snowcontrol.core.policies.engine import evaluate_policies, load_policy_config
from snowcontrol.core.render_sql import render_plan
from snowcontrol.core.state_backend import LocalStateBackend
from snowcontrol.finops.report import generate_report
from snowcontrol.utils.console import print_error, print_info, print_success

app = typer.Typer(help="SnowControl: Snowflake Control Tower")
finops_app = typer.Typer(help="FinOps analytics commands.")
app.add_typer(finops_app, name="finops")

DEFAULT_CONFIG = "snowcontrol.yaml"
DEFAULT_POLICY = "policies.yaml"


def _handle_error(exc: Exception) -> None:
    print_error(str(exc))
    raise typer.Exit(code=1)


@app.command()
def init(path: Path = Path(".")) -> None:
    """Create example config and policy files."""
    example_dir = Path(__file__).resolve().parents[2] / "examples" / "acme_account"
    for filename in ["desired.yaml", "policies.yaml"]:
        content = (example_dir / filename).read_text(encoding="utf-8")
        target = path / ("snowcontrol.yaml" if filename == "desired.yaml" else filename)
        target.write_text(content, encoding="utf-8")
    print_success("Initialized example configuration in current directory.")


@app.command()
def validate(
    config: Path = Path(DEFAULT_CONFIG),
    policy: Path = Path(DEFAULT_POLICY),
) -> None:
    """Validate config and run policy checks."""
    try:
        desired = load_config(config)
        policy_config = load_policy_config(policy)
        plan = diff_state({"resources": {}}, desired)
        results = evaluate_policies(desired, plan, BUILTIN_POLICIES, policy_config)
    except Exception as exc:  # noqa: BLE001
        _handle_error(exc)
    if results:
        print_error("Policy violations found:")
        for result in results:
            print_error(f"[{result.severity}] {result.message}")
        raise typer.Exit(code=2)
    print_success("Configuration and policies validated.")


@app.command()
def plan(
    config: Path = Path(DEFAULT_CONFIG),
    state_path: Path = Path(".snowcontrol/state.json"),
) -> None:
    """Show plan diff."""
    try:
        desired = load_config(config)
        backend = LocalStateBackend(state_path)
        current = backend.load()
        actions = diff_state(current, desired)
    except Exception as exc:  # noqa: BLE001
        _handle_error(exc)
    print_info(json.dumps(actions_to_payload(actions), indent=2))


@app.command()
def render(
    config: Path = Path(DEFAULT_CONFIG),
    state_path: Path = Path(".snowcontrol/state.json"),
    out_path: Path = Path("out/plan.sql"),
) -> None:
    """Render SQL for the current plan."""
    try:
        desired = load_config(config)
        backend = LocalStateBackend(state_path)
        actions = diff_state(backend.load(), desired)
        sql = render_plan(actions)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(sql, encoding="utf-8")
    except Exception as exc:  # noqa: BLE001
        _handle_error(exc)
    print_success(f"SQL written to {out_path}.")


@app.command()
def apply(
    config: Path = Path(DEFAULT_CONFIG),
    state_path: Path = Path(".snowcontrol/state.json"),
    out_path: Path = Path("out/apply.sql"),
) -> None:
    """Apply plan to local state and write SQL."""
    try:
        desired = load_config(config)
        backend = LocalStateBackend(state_path)
        actions = diff_state(backend.load(), desired)
        sql = render_plan(actions)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(sql, encoding="utf-8")
        backend.apply(actions_to_payload(actions))
    except Exception as exc:  # noqa: BLE001
        _handle_error(exc)
    print_success("State updated and SQL rendered.")


@finops_app.command(name="report")
def finops_report(
    metering_path: Path = Path("data/warehouse_metering_sample.csv"),
    out_dir: Path = Path("out"),
) -> None:
    """Generate FinOps report from sample data."""
    try:
        generate_report(metering_path, out_dir)
    except Exception as exc:  # noqa: BLE001
        _handle_error(exc)
    print_success("FinOps report generated.")


@app.command()
def docs() -> None:
    """Build MkDocs site."""
    import subprocess

    result = subprocess.run(["mkdocs", "build", "-f", "docs/mkdocs.yml"], check=False)
    if result.returncode != 0:
        raise typer.Exit(code=result.returncode)
    print_success("Docs built.")


@app.command()
def demo() -> None:
    """Run an end-to-end demo."""
    with TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        init(tmp_path)
        validate(tmp_path / DEFAULT_CONFIG, tmp_path / DEFAULT_POLICY)
        plan(tmp_path / DEFAULT_CONFIG, tmp_path / ".snowcontrol/state.json")
        render(
            tmp_path / DEFAULT_CONFIG,
            tmp_path / ".snowcontrol/state.json",
            tmp_path / "out/plan.sql",
        )
        apply(
            tmp_path / DEFAULT_CONFIG,
            tmp_path / ".snowcontrol/state.json",
            tmp_path / "out/apply.sql",
        )
        plan(tmp_path / DEFAULT_CONFIG, tmp_path / ".snowcontrol/state.json")
        finops_report(Path("data/warehouse_metering_sample.csv"), tmp_path / "out")
    print_success("Demo complete.")
