import { ChartsGenericView } from "scenes/Dashboard/containers/ChartsGenericView";

describe("ChartsGenericView", (): void => {
  it("should return an function", (): void => {
    expect.hasAssertions();
    expect(typeof ChartsGenericView).toStrictEqual("function");
  });
});
