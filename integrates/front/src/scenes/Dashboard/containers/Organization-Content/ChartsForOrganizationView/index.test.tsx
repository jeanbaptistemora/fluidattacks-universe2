import { ChartsForOrganizationView } from "scenes/Dashboard/containers/Organization-Content/ChartsForOrganizationView";

describe("ChartsForOrganizationView", (): void => {
  it("should return an function", (): void => {
    expect.hasAssertions();
    expect(typeof ChartsForOrganizationView).toBe("function");
  });
});
