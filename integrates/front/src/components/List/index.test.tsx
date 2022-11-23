import { List } from ".";

describe("List", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof List).toBe("function");
  });
});
