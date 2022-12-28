import { ChartsForGroupView } from "scenes/Dashboard/containers/Group-Content/ChartsForGroupView";

describe("ChartsForGroupView", (): void => {
  it("should return an function", (): void => {
    expect.hasAssertions();
    expect(typeof ChartsForGroupView).toBe("function");
  });
});
