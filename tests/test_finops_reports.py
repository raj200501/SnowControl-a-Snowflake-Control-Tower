from pathlib import Path

from snowcontrol.finops.report import generate_report


def test_generate_report(tmp_path: Path) -> None:
    report = generate_report(Path("data/warehouse_metering_sample.csv"), tmp_path)
    assert "top_warehouses" in report
    assert (tmp_path / "finops_report.json").exists()
    assert (tmp_path / "finops_report.md").exists()
