import { render } from "@testing-library/react-native";
import React from "react";

import { Logo } from ".";

describe("Logo", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof Logo).toBe("function");
  });

  it("should render", (): void => {
    expect.hasAssertions();

    const component = render(
      <Logo fill={"#FFFFFF"} height={125} width={300} />
    );

    expect(component).toBeDefined();
  });
});
