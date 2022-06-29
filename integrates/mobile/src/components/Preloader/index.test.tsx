import { render } from "@testing-library/react-native";
import React from "react";

import { Preloader } from ".";

describe("Preloader", (): void => {
  it("should return a function", (): void => {
    expect.hasAssertions();

    expect(typeof Preloader).toBe("function");
  });

  it("should render", (): void => {
    expect.hasAssertions();

    const component = render(<Preloader visible={true} />);

    expect(component).toBeDefined();
  });
});
