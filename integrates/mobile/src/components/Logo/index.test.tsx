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

    const component = <Logo fill={"#FFFFFF"} height={125} width={300} />;

    const { getByTestId } = render(component);

    expect(getByTestId("logo")).toBeDefined();
  });
});
