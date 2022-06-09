import { Input } from ".";

describe("Input", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Input).toBe("function");
  });
});
