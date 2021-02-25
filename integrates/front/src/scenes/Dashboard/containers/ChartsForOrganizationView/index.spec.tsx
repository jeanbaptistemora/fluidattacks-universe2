import { ChartsForOrganizationView } from "scenes/Dashboard/containers/ChartsForOrganizationView";

describe("ChartsForOrganizationView", (): void => {
  it("should return an function", (): void => {
    expect.hasAssertions();
    expect(typeof ChartsForOrganizationView).toStrictEqual("function");
  });
});
