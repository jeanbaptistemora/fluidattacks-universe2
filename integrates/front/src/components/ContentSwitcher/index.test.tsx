import { ContentSwitcher } from ".";

describe("ContentSwitcher", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof ContentSwitcher).toBe("function");
  });
});
