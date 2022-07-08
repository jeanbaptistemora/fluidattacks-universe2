import { EventBar } from "scenes/Dashboard/components/EventBar";

describe("EventBar", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof EventBar).toBe("function");
  });
});
