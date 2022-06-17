import { Accordion } from ".";

describe("Accordion", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();
    expect(typeof Accordion).toBe("function");
  });
});
