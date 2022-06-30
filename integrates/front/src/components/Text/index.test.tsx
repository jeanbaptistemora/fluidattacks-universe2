import { Text } from ".";

describe("Text", (): void => {
  it("should return an object", (): void => {
    expect.hasAssertions();
    expect(typeof Text).toBe("object");
  });
});
