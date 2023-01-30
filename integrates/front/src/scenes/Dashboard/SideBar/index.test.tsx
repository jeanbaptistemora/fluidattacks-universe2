import { DashboardSideBar } from ".";

describe("Dashboard", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof DashboardSideBar).toBe("function");
  });
});
