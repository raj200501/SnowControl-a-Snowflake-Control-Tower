import { render, screen } from "@testing-library/react";

import { KpiCard } from "./KpiCard";

describe("KpiCard", () => {
  it("renders title and value", () => {
    render(<KpiCard title="Credits" value="120" trend="Up" />);
    expect(screen.getByText("Credits")).toBeInTheDocument();
    expect(screen.getByText("120")).toBeInTheDocument();
    expect(screen.getByText("Up")).toBeInTheDocument();
  });
});
