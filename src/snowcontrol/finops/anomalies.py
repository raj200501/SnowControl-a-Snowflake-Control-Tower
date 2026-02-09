from __future__ import annotations

from statistics import mean, pstdev


def z_score_flags(values: dict[str, float], threshold: float = 2.0) -> list[str]:
    if not values:
        return []
    data = list(values.values())
    avg = mean(data)
    deviation = pstdev(data) or 1.0
    flagged = []
    for day, value in values.items():
        z_score = (value - avg) / deviation
        if z_score >= threshold:
            flagged.append(day)
    return flagged
