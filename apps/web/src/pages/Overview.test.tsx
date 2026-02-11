import { render, screen, waitFor } from "@testing-library/react";
import { vi } from "vitest";

import { OverviewPage } from "./Overview";

const mockOverview = {
  credits_today: 12.4,
  p95_latency_today_ms: 880,
  anomaly_count: 2,
  governance_issue_count: 1,
};

const mockMetering = [
  {
    id: 1,
    warehouse_name: "WH_CORE",
    start_time: "2024-01-01T00:00:00",
    end_time: "2024-01-01T02:00:00",
    credits_used: 4.2,
  },
];

vi.mock("../api/client", () => ({
  api: {
    overview: () => Promise.resolve(mockOverview),
    metering: () => Promise.resolve(mockMetering),
  },
}));

describe("OverviewPage", () => {
  it("renders KPIs", async () => {
    render(<OverviewPage />);
    await waitFor(() => expect(screen.getByText("Credits / Day")).toBeInTheDocument());
    expect(screen.getByText("12.4")).toBeInTheDocument();
    expect(screen.getByText("880 ms")).toBeInTheDocument();
  });
});
