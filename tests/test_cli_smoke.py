from pathlib import Path

from typer.testing import CliRunner

from snowcontrol.cli import app


def test_cli_demo_flow() -> None:
    runner = CliRunner()
    metering_path = Path(__file__).resolve().parents[1] / "data" / "warehouse_metering_sample.csv"
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["init"])
        assert result.exit_code == 0
        result = runner.invoke(app, ["validate"])
        assert result.exit_code == 0
        result = runner.invoke(app, ["plan"])
        assert result.exit_code == 0
        result = runner.invoke(app, ["render"])
        assert result.exit_code == 0
        result = runner.invoke(app, ["apply"])
        assert result.exit_code == 0
        result = runner.invoke(
            app, ["finops", "report", "--metering-path", str(metering_path)]
        )
        assert result.exit_code == 0
