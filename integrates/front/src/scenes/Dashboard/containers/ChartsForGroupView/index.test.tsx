import { ChartsForGroupView } from "scenes/Dashboard/containers/ChartsForGroupView";

describe("ChartsForGroupView", (): void => {
  it("should return an function", (): void => {
    expect.hasAssertions();
    expect(typeof ChartsForGroupView).toBe("function");
  });
});
