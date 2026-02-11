import { api, TOKEN } from "./client";
import { vi } from "vitest";

describe("api client", () => {
  it("adds Authorization header", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({}),
    });
    globalThis.fetch = fetchMock as unknown as typeof fetch;
    await api.overview();
    expect(fetchMock).toHaveBeenCalledWith(expect.stringContaining("/api/v1/overview"), {
      headers: { Authorization: `Bearer ${TOKEN}` },
    });
  });
});
